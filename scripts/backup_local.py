"""Run from repository root with PYTHONPATH=backend. Never print connection secrets."""

import argparse
import json
from pathlib import Path

from app.backup import create_backup, read_backup, restore_backup
from app.config import Settings
from app.db import make_engine


def main():
    parser = argparse.ArgumentParser(description="Chef Core logical backup and isolated recovery")
    sub = parser.add_subparsers(dest="operation", required=True)
    backup = sub.add_parser("create")
    backup.add_argument("archive", type=Path)
    verify = sub.add_parser("verify")
    verify.add_argument("archive", type=Path)
    restore = sub.add_parser("restore")
    restore.add_argument("archive", type=Path)
    restore.add_argument("--vault-target", type=Path, required=True)
    args = parser.parse_args()
    settings = Settings()
    engine = None
    try:
        if args.operation == "verify":
            manifest, _ = read_backup(args.archive)
            result = {"status": "verified", "row_counts": manifest["row_counts"]}
        else:
            engine = make_engine(settings.database_url)
            if args.operation == "create":
                manifest = create_backup(
                    engine,
                    settings.vault_root,
                    args.archive,
                    Path(__file__).resolve().parents[1] / "docs" / "CHEF_CONSTITUTION_0_1.md",
                )
                result = {"status": "created", "row_counts": manifest["row_counts"]}
            else:
                result = restore_backup(engine, args.archive, args.vault_target)
        print(json.dumps(result))
    except Exception as exc:  # noqa: BLE001 -- CLI boundary; suppress connection strings and personal content
        print(
            json.dumps(
                {
                    "status": "failed",
                    "error_type": type(exc).__name__,
                    "next_action": "Inspect target and operator guide; no overwrite or automatic cleanup performed.",
                }
            )
        )
        raise SystemExit(1) from None
    finally:
        if engine is not None:
            engine.dispose()


if __name__ == "__main__":
    main()
