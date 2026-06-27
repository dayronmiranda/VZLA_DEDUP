"""Tests de equivalencia del HMAC de PII unificado (issue #30).

Verifican que el redactor (scrapers.sanitizers.pii_tokenizer.hmac_token) y el
matcher (shared.hashing.identity_token) comparten UNA sola normalización
canónica, de modo que la MISMA cédula en formatos distintos produce el MISMO
token.

Se usa `monkeypatch.setenv` para no filtrar PII_HMAC_SECRET a otras suites
(p.ej. test_sanitizer.py, que asume el redactor SIN secret).
"""

from __future__ import annotations

from scrapers.sanitizers.pii_tokenizer import HMAC_PREFIX, hmac_digest, hmac_token
from shared.hashing import hmac_hex, identity_token, normalize_identifier


SECRET = "test-secret-unified"


def test_redactor_and_matcher_produce_same_token(monkeypatch):
    monkeypatch.setenv("PII_HMAC_SECRET", SECRET)

    redactor_token = hmac_token("V-12.345.678").removeprefix(HMAC_PREFIX)
    matcher_token = identity_token("V12345678", SECRET)

    assert redactor_token == matcher_token


def test_different_formats_collapse_to_same_token(monkeypatch):
    monkeypatch.setenv("PII_HMAC_SECRET", SECRET)

    formats = ["V-12.345.678", "V12345678", "v 12 345 678", "V.12.345.678"]
    tokens = {hmac_token(value).removeprefix(HMAC_PREFIX) for value in formats}

    assert len(tokens) == 1


def test_hmac_digest_matches_identity_token(monkeypatch):
    monkeypatch.setenv("PII_HMAC_SECRET", SECRET)

    assert hmac_digest("V-12.345.678") == identity_token("V12345678", SECRET)


def test_redactor_delegates_to_shared_hmac_hex(monkeypatch):
    monkeypatch.setenv("PII_HMAC_SECRET", SECRET)

    assert hmac_token("V12345678").removeprefix(HMAC_PREFIX) == hmac_hex("V-12.345.678", SECRET)


def test_normalize_identifier_strips_punctuation_and_spaces():
    assert normalize_identifier("V-12.345.678") == normalize_identifier("V12345678")
    assert normalize_identifier("V-12.345.678") == "v12345678"
