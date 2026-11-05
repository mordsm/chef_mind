"""Scoped cooking guidance from source-checked notes in the existing ontology.

Only the curated manifest is executable data. Markdown bodies stay inert, and
culinary temperatures never become food-safety thresholds or observations.
"""

import json
import re
from functools import lru_cache
from pathlib import Path

import yaml

from app.ontology_bridge import DEFAULT_VAULT_ROOT, _parse_markdown_file


def _normalized(text):
    return " ".join(re.findall(r"[\w]+", text.casefold()))


@lru_cache(maxsize=1)
def _index(signature):
    root = DEFAULT_VAULT_ROOT / "Culinary-Knowledge"
    nodes = []
    for node_id, digest, path, _, _ in signature:
        node = _parse_markdown_file(Path(path), root)
        if (node and node["id"] == node_id and node["sha256"] == digest
                and node["metadata"].get("source_text_checked") is True
                and node["metadata"].get("project_scope", "chef_mind") == "chef_mind"):
            nodes.append(node)
    return tuple(nodes)


def _signature(root):
    records = []
    for relative in ("09_Sources/Supplied-2026/manifest.json", "09_Sources/Full-Books/reviewed-manifest.json"):
        manifest_path = root / relative
        if not manifest_path.exists():
            continue
        records.extend(json.loads(manifest_path.read_text(encoding="utf-8"))["records"])
    signature = []
    for record in records:
        path = (root / record.get("path", f"03_Techniques/{record['id']}.md")).resolve()
        path.relative_to(root.resolve())
        stat = path.stat()
        signature.append((record["id"], record["sha256"], str(path), stat.st_mtime_ns, stat.st_size))
    return tuple(signature)


def practical_knowledge(query, method=""):
    """Exact ingredient/phrase scope plus optional canonical method constraint."""
    root = DEFAULT_VAULT_ROOT / "Culinary-Knowledge"
    try:
        nodes = _index(_signature(root))
    except (OSError, ValueError, KeyError, yaml.YAMLError):
        return []
    text = " " + _normalized(query) + " "
    matches = []
    for node in nodes:
        meta = node["metadata"]
        if not any(" " + _normalized(alias) + " " in text for alias in meta.get("target_foods", [])):
            continue
        conditions = meta.get("conditions", {})
        if conditions.get("method_id") and conditions["method_id"] != method:
            continue
        aliases = [len(_normalized(alias)) for alias in meta.get("target_foods", [])
                   if " " + _normalized(alias) + " " in text]
        overlap = set(_normalized(query).split()) & set(_normalized(meta.get("chef_tip", "") + " " + node["name"]).split())
        matches.append((max(aliases) + 2 * len(overlap), node))
    matches.sort(key=lambda pair: pair[0], reverse=True)
    return [node for _, node in matches]


def practical_tips(query, method=""):
    result = []
    for node in practical_knowledge(query, method):
        meta = node["metadata"]
        ref = meta["sources"][0]
        result.append({
            "title": node["title_he"], "text": meta["chef_tip"], "practical": True,
            "source": f"{ref['citation']} | {ref['split_filename']} | עמוד בחלק {ref['split_page']}"
                      f" | {node['relative_path']} | sha256:{node['sha256']}",
            "origin": "OBSIDIAN_SUPPLIED", "source_ids": [ref["source_id"], node["id"]],
            "step_keywords": meta.get("step_keywords", []),
        })
    return result


def cooking_defaults(query, method):
    for node in practical_knowledge(query, method):
        meta = node["metadata"]
        c = meta.get("conditions", {})
        temperature = c.get("oven_temperature_c")
        if type(temperature) not in (float, int) or not 100 <= temperature <= 250:
            continue
        result = {
            "temperature": temperature,
            "equipment": " / ".join(meta.get("recommended_equipment", [])),
            "assumption": meta["description"], "checkpoints": meta.get("checkpoints", []),
            "source": meta["sources"][0]["citation"], "source_ids": [node["id"]],
        }
        minutes = c.get("duration_minutes")
        if type(minutes) in (float, int) and 1 <= minutes <= 240:
            result["minutes"] = minutes
        if c.get("oven_program") in ("טורבו", "חום עליון ותחתון"):
            result["program"] = c["oven_program"]
        return result
    return {}


def step_guidance(query, method, instruction, *, checks=False):
    """Return only a dish-scoped note applicable to the current operation."""
    tips = practical_tips(query, method)
    nodes = {node["id"]: node for node in practical_knowledge(query, method)}
    for tip in tips:
        if not any(word in instruction for word in tip["step_keywords"]):
            continue
        if checks:
            tip["text"] = " · ".join(nodes[tip["source_ids"][1]]["metadata"].get("checkpoints", []))
        if tip["text"]:
            return tip
    return None
