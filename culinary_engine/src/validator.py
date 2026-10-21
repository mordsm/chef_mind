"""Strict source validation; undefined methods fail closed at decision time."""

import re

import yaml


class UniqueLoader(yaml.SafeLoader):
    pass


def mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key in result:
            raise ValueError("YAML keys must be unique strings")
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def parse(raw):
    if not isinstance(raw, str) or len(raw.encode("utf-8")) > 256_000:
        raise ValueError("Source exceeds 256 KB")
    try:
        # References are unnecessary in these editable source documents.
        if any(
            isinstance(token, (yaml.tokens.AliasToken, yaml.tokens.AnchorToken)) for token in yaml.scan(raw)
        ):
            raise ValueError("YAML aliases are not supported")
        data = yaml.load(raw, Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise ValueError("Invalid YAML") from exc
    if not isinstance(data, dict):
        raise ValueError("Expected a YAML mapping")  # noqa: TRY004 - unified validation exception
    return data


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,79}", value):
        raise ValueError("Invalid identifier")


def text(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 2000:
        raise ValueError("Expected nonempty text of at most 2000 characters")


def validate(rules, registry):
    if set(rules) != {"universal_methods", "failure_reasons", "archetypes"}:
        raise ValueError("Expected universal_methods, failure_reasons and archetypes")
    methods = rules["universal_methods"]
    if not isinstance(methods, list) or not methods or any(not isinstance(x, str) for x in methods):
        raise ValueError("Expected method identifiers")
    if len(set(methods)) != len(methods):
        raise ValueError("Duplicate methods")
    for method in methods:
        identifier(method)
    reasons, families = rules["failure_reasons"], rules["archetypes"]
    if not isinstance(reasons, dict) or not isinstance(families, dict) or not families:
        raise ValueError("Expected reasons and families mappings")
    for reason in reasons.values():
        if not isinstance(reason, dict) or set(reason) != {"code", "message"}:
            raise ValueError("Each reason requires code and message")
        text(reason["code"])
        text(reason["message"])
    for key, family in families.items():
        identifier(key)
        if not isinstance(family, dict) or set(family) != {"name", "allowed_methods", "blocked_methods"}:
            raise ValueError("Invalid family fields")
        text(family["name"])
        allowed, blocked = family["allowed_methods"], family["blocked_methods"]
        if not isinstance(allowed, list) or any(not isinstance(x, str) for x in allowed):
            raise ValueError("Expected allowed method list")
        if not isinstance(blocked, dict) or len(allowed) != len(set(allowed)):
            raise ValueError("Duplicate methods or invalid blocked mapping")
        if set(allowed) & set(blocked) or not set(allowed + list(blocked)) <= set(methods):
            raise ValueError("Conflicting or unknown method references")
        if any(not isinstance(x, str) or x not in reasons for x in blocked.values()):
            raise ValueError("Unknown failure reason")
    if set(registry) != {"ingredients"} or not isinstance(registry["ingredients"], dict):
        raise ValueError("Expected ingredients mapping")
    for key, ingredient in registry["ingredients"].items():
        identifier(key)
        if not isinstance(ingredient, dict) or set(ingredient) != {"name", "archetype"}:
            raise ValueError("Each ingredient requires name and archetype")
        text(ingredient["name"])
        if not isinstance(ingredient["archetype"], str) or ingredient["archetype"] not in families:
            raise ValueError("Unknown ingredient archetype")
