"""Create private local configuration once; never print or overwrite credentials."""

import json
import secrets
from pathlib import Path


def main():
    target = Path(".env")
    if target.exists():
        print("Local .env already exists; preserved unchanged.")
        return
    token = secrets.token_urlsafe(36)
    keys = json.dumps({token: {"user_id": "owner", "role": "reviewer"}})
    data = (
        "CHEF_DATABASE_URL=postgresql+psycopg://chef:local-development-only@127.0.0.1:56432/chef\n"
        "CHEF_VAULT_ROOT=./vault\n"
        f"CHEF_API_KEYS={keys}\n"
        "CHEF_POLL_SECONDS=10\n"
    )
    with target.open("x", encoding="utf-8") as stream:
        stream.write(data)
    print(
        "Created ignored .env with a private owner token. Read it locally to authorize Swagger; keep it private."
    )


if __name__ == "__main__":
    main()
