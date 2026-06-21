"""Nasdaq splits — upcoming stock-split snapshot."""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import BASE, _s, _get_json, _envelope_ok


def fetch_splits(node_id: str) -> None:
    asset = node_id
    payload = _get_json(f"{BASE}/calendar/splits")
    if not _envelope_ok(payload):
        raise RuntimeError("splits calendar bad envelope")
    data = payload.get("data") or {}
    out = [{
        "symbol": _s(r.get("symbol")),
        "name": _s(r.get("name")),
        "ratio": _s(r.get("ratio")),
        "executionDate": _s(r.get("executionDate")),
    } for r in (data.get("rows") or [])]
    if not out:
        raise RuntimeError("splits calendar returned no rows")
    save_raw_ndjson(out, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="nasdaq-splits", fn=fetch_splits, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nasdaq-splits-transform",
        deps=["nasdaq-splits"],
        sql='''
            SELECT
                symbol,
                name AS company_name,
                ratio,
                try_strptime(executionDate, '%m/%d/%Y')::DATE AS execution_date
            FROM "nasdaq-splits"
            WHERE symbol IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY symbol, execution_date ORDER BY symbol
            ) = 1
        ''',
    ),
]
