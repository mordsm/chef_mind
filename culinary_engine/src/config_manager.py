"""Validated, atomic UTF-8 source updates, preserving raw YAML."""

import os
import tempfile
from copy import deepcopy
from pathlib import Path
from threading import RLock

import yaml

from .validator import parse, validate


class ConfigManager:
    def __init__(self, config_dir=None):
        self.config_dir = Path(config_dir or Path(__file__).resolve().parent.parent / "config").resolve()
        self.rules_path = self.config_dir / "culinary_rules_engine.yaml"
        self.registry_path = self.config_dir / "ingredients_registry.yaml"
        self._lock = RLock()
        self.reload()

    def reload(self):
        with self._lock:
            rules = parse(self.get_raw_rules_yaml())
            registry = parse(self.get_raw_registry_yaml())
            validate(rules, registry)
            self.rules_data, self.registry_data = rules, registry

    def get_raw_rules_yaml(self):
        return self.rules_path.read_text(encoding="utf-8-sig")

    def get_raw_registry_yaml(self):
        return self.registry_path.read_text(encoding="utf-8-sig")

    @staticmethod
    def _write(path, raw):
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=path.parent, delete=False, newline=""
            ) as stream:
                temporary = stream.name
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            if temporary and os.path.exists(temporary):
                os.unlink(temporary)

    def save_raw_rules_yaml(self, raw_content):
        with self._lock:
            rules = parse(raw_content)
            registry = parse(self.get_raw_registry_yaml())
            validate(rules, registry)
            self._write(self.rules_path, raw_content)
            self.rules_data, self.registry_data = rules, registry

    def save_raw_registry_yaml(self, raw_content):
        with self._lock:
            registry = parse(raw_content)
            rules = parse(self.get_raw_rules_yaml())
            validate(rules, registry)
            self._write(self.registry_path, raw_content)
            self.rules_data, self.registry_data = rules, registry

    def add_or_update_ingredient(self, key, name, archetype):
        with self._lock:
            registry = deepcopy(parse(self.get_raw_registry_yaml()))
            registry["ingredients"][key] = {"name": name, "archetype": archetype}
            self.save_raw_registry_yaml(yaml.safe_dump(registry, allow_unicode=True, sort_keys=False))

    def _save_registry(self):
        self.save_raw_registry_yaml(yaml.safe_dump(self.registry_data, allow_unicode=True, sort_keys=False))
