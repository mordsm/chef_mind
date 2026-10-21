"""Run with python culinary_engine/main.py [--config-dir PATH]."""

import argparse
import json

from src.config_manager import ConfigManager
from src.sous_chef import SousChefEngine


def run_demo(config_dir=None):
    config = ConfigManager(config_dir)
    chef = SousChefEngine(config)
    print(config.get_raw_registry_yaml())
    allowed = chef.get_allowed_methods("chicken_gizzard")
    print(allowed)
    assert "oven_roast_dry" not in allowed
    result = chef.validate_method_choice("chicken_gizzard", "oven_roast_dry")
    assert result["allowed"] is False and result["error_code"] == "ERR_COLLAGEN_DRY"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    config.add_or_update_ingredient("beef_tongue", "לשון בקר", "dense_collagen_lean")
    print(chef.get_allowed_methods("beef_tongue"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-dir")
    run_demo(parser.parse_args().config_dir)
