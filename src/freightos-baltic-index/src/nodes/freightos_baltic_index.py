"""Freightos Baltic Index (FBX) connector.

Source: the free public FBX charts Freightos publishes as Infogram embeds
(documented at developers.freightos.com/freight-tools). The "FBX Global" embed
is backed by an Infogram "live data" Google-Sheet sync served as a single public
JSON document at https://live-data.jifo.co/<key>. One fetch returns the full
weekly history for every public FBX index (the global FBX plus the four trade
lanes FBX01/03/11/13).

Strategy: stateless full re-pull. The corpus is ~100KB and re-fetched whole each
run, so revisions/late corrections are picked up for free — no watermark, no
cursor. The live FBX terminal (daily granularity, ~13 lanes) is commercially
gated and not used here.

URL stability: the infogram.com/_/<embed-id> id is stable (published in Freightos
docs); the live-data.jifo.co UUID is an internal sync key, so it is resolved from
the embed at runtime rather than hard-coded.
"""
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

# Stable Infogram embed id for the public "FBX Global" chart. Its backing
# "FBX Full Data" sheet carries the full weekly history for every public FBX
# index, so this single embed covers the whole corpus.
_FBX_GLOBAL_EMBED = "AcDi5xXouXrzQMLqbVpj"
_EMBED_URL = "https://infogram.com/_/" + _FBX_GLOBAL_EMBED
_LIVE_DATA_BASE = "https://live-data.jifo.co/"
_FULL_DATA_SHEET = "FBX Full Data"

# Maps the Infogram live-data sync key out of the embedded window.infographicData.
_KEY_RE = re.compile(
    r'"key"\s*:\s*"([0-9a-fA-F-]{20,})"\s*,\s*"provider"\s*:\s*"atlas_google_drive"'
)

_SCHEMA = pa.schema([
    ("date", pa.string()),        # ISO 'YYYY-MM-DD' as published
    ("index_code", pa.string()),  # FBX, FBX01, FBX03, FBX11, FBX13
    ("value", pa.float64()),      # USD spot rate per 40ft container (FEU)
])


@transient_retry()
def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _parse_money(cell) -> float | None:
    """'$1,575.60' / '2485' / '' -> float | None. Non-numeric cells -> None."""
    if cell is None:
        return None
    s = str(cell).strip()
    s = re.sub(r"[^0-9.\-]", "", s)  # drop '$', ',', whitespace
    if s in ("", "-", ".", "-."):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _resolve_full_data_grid() -> list[list]:
    """Resolve the embed to its live-data JSON and return the FBX Full Data
    sheet as a list of rows (header first)."""
    html = _get_text(_EMBED_URL)
    m = _KEY_RE.search(html)
    if not m:
        raise RuntimeError(
            "could not resolve Infogram live-data key from %s" % _EMBED_URL
        )
    payload = _get_json(_LIVE_DATA_BASE + m.group(1))
    names = payload["sheetNames"]
    if _FULL_DATA_SHEET not in names:
        raise RuntimeError(
            "'%s' sheet not present; sheets=%r" % (_FULL_DATA_SHEET, names)
        )
    return payload["data"][names.index(_FULL_DATA_SHEET)]


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    grid = _resolve_full_data_grid()
    if not grid or len(grid) < 2:
        raise RuntimeError("FBX Full Data grid empty or header-only: %r" % grid)

    header = grid[0]                       # ['Date', 'FBX', 'FBX01', ...]
    codes = [c for c in header[1:]]
    rows = []
    for record in grid[1:]:
        if not record:
            continue
        date = record[0]
        if not date:
            continue
        for col, code in enumerate(codes, start=1):
            if not code:
                continue
            cell = record[col] if col < len(record) else None
            rows.append({
                "date": str(date),
                "index_code": code,
                "value": _parse_money(cell),
            })

    table = pa.Table.from_pylist(rows, schema=_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="freightos-baltic-index-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="freightos-baltic-index-values-transform",
        deps=["freightos-baltic-index-values"],
        sql='''
            SELECT DISTINCT
                CAST(date AS DATE)    AS date,
                index_code,
                CAST(value AS DOUBLE) AS value
            FROM "freightos-baltic-index-values"
            WHERE value IS NOT NULL
              AND date IS NOT NULL
              AND index_code IS NOT NULL
        ''',
    ),
]
