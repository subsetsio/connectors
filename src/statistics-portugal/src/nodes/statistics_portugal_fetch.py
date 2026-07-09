"""Fetch helpers for Statistics Portugal indicator nodes."""
from __future__ import annotations

from typing import Any

from subsets_utils import get, save_raw_ndjson

BASE_URL = "https://www.ine.pt/ine/json_indicador/pindica.jsp"
SPEC_PREFIX = "statistics-portugal-"


def _indicator_id_from_node(node_id: str) -> str:
    if not node_id.startswith(SPEC_PREFIX):
        raise ValueError(f"unexpected statistics-portugal node id: {node_id}")
    indicator_id = node_id[len(SPEC_PREFIX):]
    if not indicator_id.isdigit() or len(indicator_id) != 7:
        raise ValueError(f"unexpected INE indicator id in node id: {node_id}")
    return indicator_id


def _value_as_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).replace(" ", "").replace(",", "."))
    except ValueError:
        return None


def _dimension_pairs(row: dict[str, Any]) -> dict[str, dict[str, Any]]:
    dimensions: dict[str, dict[str, Any]] = {}
    for key, value in row.items():
        if not key.startswith("dim_") or key.endswith("_t"):
            continue
        dim_name = key[4:]
        dimensions[dim_name] = {
            "code": value,
            "label": row.get(f"{key}_t"),
        }
    return dimensions


def _rows_from_payload(indicator_id: str, payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        raise RuntimeError(f"{indicator_id}: expected JSON list, got {type(payload).__name__}")

    rows: list[dict[str, Any]] = []
    for indicator in payload:
        if not isinstance(indicator, dict):
            raise RuntimeError(f"{indicator_id}: expected indicator object")
        dados = indicator.get("Dados") or {}
        if not isinstance(dados, dict):
            raise RuntimeError(f"{indicator_id}: expected Dados object")

        response_indicator_id = str(indicator.get("IndicadorCod") or indicator_id).zfill(7)
        for period, period_rows in dados.items():
            if period_rows is None:
                continue
            if not isinstance(period_rows, list):
                raise RuntimeError(f"{indicator_id}: expected row list for period {period}")
            for source_row in period_rows:
                if not isinstance(source_row, dict):
                    raise RuntimeError(f"{indicator_id}: expected observation object")
                rows.append({
                    "indicator_id": response_indicator_id,
                    "indicator_name": indicator.get("IndicadorDsg"),
                    "update_type": indicator.get("UltimoPref"),
                    "last_update": indicator.get("DataUltimoAtualizacao"),
                    "period": str(period),
                    "geo_code": source_row.get("geocod"),
                    "geo_label": source_row.get("geodsg"),
                    "value": _value_as_float(source_row.get("valor")),
                    "value_raw": source_row.get("valor"),
                    "value_formatted": source_row.get("ind_string"),
                    "dimensions": _dimension_pairs(source_row),
                })
    return rows


def fetch_indicator(node_id: str) -> None:
    indicator_id = _indicator_id_from_node(node_id)
    response = get(
        BASE_URL,
        params={"op": "2", "varcd": indicator_id, "Dim1": "T", "lang": "EN"},
        timeout=(10.0, 300.0),
    )
    response.raise_for_status()
    rows = _rows_from_payload(indicator_id, response.json())
    if not rows:
        raise RuntimeError(f"{indicator_id}: INE response contained no observations")
    save_raw_ndjson(rows, node_id)
