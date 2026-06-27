from __future__ import annotations

from pathlib import Path


def run_pipeline(
    config_path: Path,
    output_dir: Path,
    limit: int | None = None,
    keep_raw: bool = False,
) -> dict:
    """
    Orquestador principal del pipeline.

    Etapas pendientes de implementar:
      1. Adapters  — fetch por tipo de fuente (Playwright / httpx / BS4 / pdfplumber)
      2. Parsers   — uno por fuente, produce Person | AcopioCenter | Event
      3. Limpieza  — PII → Normalización → Dedup → Validación (en ese orden)
      4. Export    — persons.jsonl / acopio.jsonl / events.jsonl
    """
    raise NotImplementedError(
        "Pipeline pendiente de reimplementar con modelos tipados (Person, AcopioCenter, Event). "
        "Ver spec: docs/pipeline.svg"
    )


def _stub_summary() -> dict:
    """Devuelve un summary vacío con las keys que espera cli.py."""
    return {
        "sources_processed": 0,
        "documents_exported": 0,
        "claims_exported": 0,
        "claims_deduplicated": 0,
        "errors": [],
    }