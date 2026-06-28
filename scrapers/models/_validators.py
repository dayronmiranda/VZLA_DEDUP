from __future__ import annotations

import uuid


def validate_uuid_str(v: str) -> str:
    """Raise ValueError if ``v`` is not a valid UUID string."""
    try:
        uuid.UUID(v)
    except (ValueError, AttributeError, TypeError) as exc:
        raise ValueError("must be a valid UUID string") from exc
    return v
