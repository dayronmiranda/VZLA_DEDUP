from __future__ import annotations

import hashlib
import hmac

from scrapers.normalizers.text import normalize_for_match


def sha256_hex(text: str | None) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def normalize_identifier(raw: str | None) -> str:
    """Normalización canónica única para PII (cédulas, teléfonos).

    Quita puntuación, espacios y acentos para que distintos formatos de la
    misma cédula ("V-12.345.678", "V12345678", "v 12 345 678") colapsen al
    mismo valor. Esta es la ÚNICA normalización usada antes de tokenizar PII,
    compartida por el redactor (hmac_token) y el matcher (identity_token).
    """
    return normalize_for_match(raw).replace(" ", "")


def hmac_hex(value: str | None, secret: str) -> str | None:
    """HMAC-SHA256 determinista sobre el identificador normalizado canónicamente.

    - Exige `secret` (ValueError si falta).
    - Devuelve None si el valor queda vacío tras normalizar.
    """
    if not secret:
        raise ValueError("Se requiere PII_HMAC_SECRET para tokenizar identidad")

    normalized = normalize_identifier(value)
    if not normalized:
        return None
    return hmac.new(secret.encode("utf-8"), normalized.encode("utf-8"), hashlib.sha256).hexdigest()


def identity_token(raw_identifier: str | None, secret: str) -> str | None:
    """HMAC determinista de un documento de identidad (cédula) -> `cedula_hmac`.

    Señal decisiva para deduplicar personas sin almacenar la PII cruda.
    Se normaliza antes para que "V-12.345.678" y "V12345678" produzcan el mismo token.
    Debe computarse en cuarentena, ANTES de redactar.

    Delega en `hmac_hex` para garantizar UNA sola normalización canónica
    compartida con el redactor.
    """
    return hmac_hex(raw_identifier, secret)
