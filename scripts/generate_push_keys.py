"""Generate a private VAPID key locally; print only its public browser key."""

import argparse
import base64
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, default=Path(".runtime/webpush-private.pem"))
args = parser.parse_args()
args.output.parent.mkdir(parents=True, exist_ok=True)
private = ec.generate_private_key(ec.SECP256R1())
with args.output.open("xb") as target:
    target.write(
        private.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
        )
    )
public = private.public_key().public_bytes(
    serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint
)
print("CHEF_PUSH_VAPID_PUBLIC_KEY=" + base64.urlsafe_b64encode(public).decode().rstrip("="))
print(
    "Private key saved locally. Set CHEF_PUSH_VAPID_PRIVATE_KEY_FILE to its absolute path; do not publish it."
)
