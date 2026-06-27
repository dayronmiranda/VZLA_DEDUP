from __future__ import annotations

import os

from shared.hashing import hmac_hex


HMAC_PREFIX = "hmac_sha256:"


def hmac_token(value: str, secret_env: str = "PII_HMAC_SECRET") -> str:
    secret = os.getenv(secret_env)
    if not secret:
        raise RuntimeError(
            f"Falta variable {secret_env}. No uses hash simple para cédulas/teléfonos."
        )
    digest = hmac_hex(value, secret)
    return f"{HMAC_PREFIX}{digest or ''}"


def hmac_digest(value: str, secret_env: str = "PII_HMAC_SECRET") -> str:
    return hmac_token(value, secret_env=secret_env).removeprefix(HMAC_PREFIX)
