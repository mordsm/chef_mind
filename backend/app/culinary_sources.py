"""User-owned source drafts. These never replace the curated coaching graph."""

import hashlib
from pathlib import Path
from typing import Literal

import yaml
from fastapi import Depends
from pydantic import Field
from sqlalchemy import select

from app.db import CulinarySourceRevision
from app.knowledge import DomainError, audit
from app.schemas import StrictModel

SourceKey = Literal["graph", "domain"]
FILES = {key: Path(__file__).with_name("data") / f"culinary_{key}_source.yaml" for key in ("graph", "domain")}
LIMIT = 262_144


class SourceUpdate(StrictModel):
    expected_revision: int = Field(ge=0)
    yaml_text: str = Field(min_length=1, max_length=LIMIT)


class EntryAddition(StrictModel):
    expected_revision: int = Field(ge=0)
    section: str = Field(min_length=1, max_length=80)
    entry_id: str | None = Field(default=None, pattern=r"^[a-z][a-z0-9_]{0,79}$")
    yaml_text: str = Field(min_length=1, max_length=LIMIT)


class DraftLoader(yaml.SafeLoader):
    """Reject duplicate keys without rejecting the originals' merge overrides."""

    def construct_mapping(self, node, deep=False):
        seen = set()
        for key, _ in node.value:
            if key.tag == "tag:yaml.org,2002:merge":
                continue
            value = self.construct_object(key, deep=False)
            if not isinstance(value, str) or value in seen:
                raise ValueError("Keys must be unique strings")
            seen.add(value)
        return super().construct_mapping(node, deep=deep)


def parse(text):
    try:
        if len(text.encode("utf-8")) > LIMIT:
            raise ValueError("Source exceeds 256 KiB")
        # Bound aliases/nesting before constructing objects; allow existing inheritance.
        depth = 0
        for count, event in enumerate(yaml.parse(text), 1):
            if isinstance(event, (yaml.MappingStartEvent, yaml.SequenceStartEvent)):
                depth += 1
            if isinstance(event, (yaml.MappingEndEvent, yaml.SequenceEndEvent)):
                depth -= 1
            if depth > 30 or count > 30000:
                raise ValueError("Source is too complex")
        data = yaml.load(text, Loader=DraftLoader)
        visited = set()

        def check(value, ancestors=()):
            if isinstance(value, (dict, list)):
                if id(value) in ancestors:
                    raise ValueError("Recursive aliases are not supported")
                if id(value) in visited:
                    return
                for child in value.values() if isinstance(value, dict) else value:
                    check(child, (*ancestors, id(value)))
                visited.add(id(value))

        check(data)
        return data
    except (yaml.YAMLError, ValueError, TypeError, RecursionError) as exc:
        raise DomainError(
            "INVALID_YAML", "Use valid YAML with unique string keys and no recursive aliases", 422
        ) from exc


def validate(key, text):
    data = parse(text)
    sections = {
        "base_ingredients",
        "cooking_methods",
        "recipe_paths",
        "archetypes" if key == "domain" else "preparations",
    }
    if not isinstance(data, dict) or set(data) != sections:
        raise DomainError("INVALID_SOURCE", "Keep the four original top-level source sections", 422)
    for section, entries in data.items():
        if not isinstance(entries, list if section == "recipe_paths" else dict):
            raise DomainError(
                "INVALID_SOURCE", "recipe_paths must be a list; other sections must be mappings", 422
            )
        values = entries if isinstance(entries, list) else entries.values()
        if any(not isinstance(entry, dict) for entry in values):
            raise DomainError("INVALID_SOURCE", "Each source entry must be a mapping", 422)
    for entry in data["recipe_paths"]:
        for field, section in (("ingredient_ref", "base_ingredients"), ("method_ref", "cooking_methods")):
            if not isinstance(entry.get(field), str) or entry[field] not in data[section]:
                raise DomainError(
                    "INVALID_REFERENCE", "Recipe paths must reference existing ingredients and methods", 422
                )
        if key == "domain" and (
            not isinstance(entry.get("archetype_ref"), str)
            or entry["archetype_ref"] not in data["archetypes"]
        ):
            raise DomainError("INVALID_REFERENCE", "Recipe paths must reference an existing archetype", 422)
    return data


def payload(key, text, number):
    data = validate(key, text)
    return {
        "source_key": key,
        "filename": FILES[key].name,
        "revision": number,
        "yaml_text": text,
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "sections": {name: len(entries) for name, entries in data.items()},
        "status": "source_draft",
        "used_by_coach": False,
    }


def current(session, owner, key, number=None):
    query = select(CulinarySourceRevision).where(
        CulinarySourceRevision.owner_id == owner, CulinarySourceRevision.source_key == key
    )
    if number is not None:
        query = query.where(CulinarySourceRevision.number == number)
    row = session.scalar(query.order_by(CulinarySourceRevision.number.desc()).limit(1))
    if number not in (None, 0) and row is None:
        raise DomainError("NOT_FOUND", "Source revision was not found", 404)
    text = row.yaml_text if row and number != 0 else FILES[key].read_text(encoding="utf-8-sig")
    return payload(key, text, row.number if row and number != 0 else 0)


def save(session, owner, key, expected, text):
    previous = current(session, owner, key)
    if previous["revision"] != expected:
        raise DomainError("SOURCE_CONFLICT", "Source changed; reload before saving", 409)
    validate(key, text)
    if previous["yaml_text"] == text:
        return previous
    session.add(CulinarySourceRevision(owner_id=owner, source_key=key, number=expected + 1, yaml_text=text))
    audit(session, owner, "culinary_source_saved", source_key=key, revision=expected + 1)
    session.commit()
    return current(session, owner, key)


def install_source_routes(app, db, principal, reviewer):
    @app.get("/v1/culinary/templates/{key}")
    def template(key: SourceKey):
        return payload(key, FILES[key].read_text(encoding="utf-8-sig"), 0)

    @app.get("/v1/culinary/sources")
    def sources(session=Depends(db), owner=Depends(principal)):
        return {
            "items": [
                {k: v for k, v in current(session, owner.user_id, key).items() if k != "yaml_text"}
                for key in FILES
            ]
        }

    @app.get("/v1/culinary/sources/{key}")
    def read(key: SourceKey, revision: int | None = None, session=Depends(db), owner=Depends(principal)):
        if revision is not None and revision < 0:
            raise DomainError("INVALID_REVISION", "Revision must be nonnegative", 422)
        return current(session, owner.user_id, key, revision)

    @app.put("/v1/culinary/sources/{key}")
    def replace(key: SourceKey, body: SourceUpdate, session=Depends(db), owner=Depends(reviewer)):
        return save(session, owner.user_id, key, body.expected_revision, body.yaml_text)

    @app.post("/v1/culinary/sources/{key}/entries", status_code=201)
    def add(key: SourceKey, body: EntryAddition, session=Depends(db), owner=Depends(reviewer)):
        previous = current(session, owner.user_id, key)
        data = validate(key, previous["yaml_text"])
        entry = parse(body.yaml_text)
        if body.section not in data or not isinstance(entry, dict):
            raise DomainError("INVALID_ENTRY", "Choose an existing section and provide a YAML mapping", 422)
        if body.section == "recipe_paths":
            if body.entry_id is not None:
                raise DomainError("INVALID_ENTRY", "Recipe paths are appended without an entry_id", 422)
            data[body.section].append(entry)
        else:
            if body.entry_id is None:
                raise DomainError("INVALID_ENTRY", "Mapping entries require an entry_id", 422)
            if body.entry_id in data[body.section]:
                raise DomainError("ENTRY_EXISTS", "Entry already exists; edit the source to update it", 409)
            data[body.section][body.entry_id] = entry
        text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
        return save(session, owner.user_id, key, body.expected_revision, text)
