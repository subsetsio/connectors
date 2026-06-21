"""Shared HTTP + parsing helpers for the WIPO IP Statistics connector.

Source: the JSON+CSV REST backend of the WIPO IP Statistics Data Center
(Angular SPA at www3.wipo.int/ipstats), base
``https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public``. No auth; every
request carries ``?lang=en`` and an ``Accept-Language: en`` header (JSON
endpoints additionally need ``Accept: application/json``).

This module holds only the cross-subset machinery: the JSON client, the
office x origin x year table parser shared by the ips-search and pmh-search
subsets, the long-format schema they share, and the column helpers used by all
three sub-modules. The per-subset fetch bodies, the key-indicator schema/parser,
and every NodeSpec live in the ``nodes/`` files.
"""

import pyarrow as pa

from subsets_utils import get, transient_retry

BASE = "https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public"
JSON_HEADERS = {"Accept": "application/json", "Accept-Language": "en"}

# Long-format schema shared by the ips-search and pmh-search subsets.
IPS_SCHEMA = pa.schema([
    ("office", pa.string()),
    ("origin", pa.string()),
    ("indicator_id", pa.int32()),
    ("indicator", pa.string()),
    ("report_type", pa.string()),
    ("year", pa.int32()),
    ("breakdown_index", pa.int32()),
    ("value", pa.float64()),
])

# Transform SQL shared by the office x origin x year (ips/pmh) subsets.
OFFICE_SQL = '''
    SELECT
        office,
        origin,
        indicator_id,
        indicator,
        report_type,
        CAST(year AS INTEGER)          AS year,
        breakdown_index,
        CAST(value AS DOUBLE)          AS value
    FROM "{dep}"
    WHERE value IS NOT NULL
'''


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #


@transient_retry()
def get_json(path: str, params: dict):
    """GET a JSON endpoint under BASE, with lang=en forced on."""
    merged = dict(params)
    merged["lang"] = "en"
    resp = get(f"{BASE}/{path}", params=merged, headers=JSON_HEADERS, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #
def explode(raw) -> list[tuple[int, float]]:
    """Split a (possibly comma-packed) cell into (position, value) pairs.

    A cell is either empty/None (no observation), a single number, or several
    numbers comma-joined (a resident/non-resident/total style breakdown). The
    lang=en backend uses '.' for decimals, so ',' is unambiguously the packing
    separator. Empty/non-numeric parts are skipped but the position index is
    preserved.
    """
    if raw is None:
        return []
    s = str(raw).strip()
    if not s:
        return []
    out: list[tuple[int, float]] = []
    for idx, part in enumerate(s.split(",")):
        part = part.strip()
        if not part:
            continue
        try:
            out.append((idx, float(part)))
        except ValueError:
            continue
    return out


def year_columns(columns: list[dict]) -> list[tuple[str, int]]:
    """The numeric (value-bearing) columns whose code is a plain 4-digit year."""
    out = []
    for col in columns or []:
        code = col.get("code")
        if col.get("type") == "number" and isinstance(code, str) and code.isdigit():
            out.append((code, int(code)))
    return out


def seqorder_value(rec: dict, code: str) -> list[tuple[int, float]]:
    """Single clean numeric value from the ``<code>_SeqOrder`` companion field.

    Used for endpoints that format the display cell with thousands separators
    (pmh table-result, keyindicator keysearch-json), where ``_SeqOrder`` holds
    the unformatted number and each (row, year) carries exactly one value.
    """
    raw = rec.get(f"{code}_SeqOrder")
    if raw is None or raw == "":
        return []
    try:
        return [(0, float(raw))]
    except (TypeError, ValueError):
        return []


def parse_office_table(data: dict, indicator_id: int, indicator: str,
                       report_type: str, *, packed: bool) -> list[dict]:
    """Parse an ips/pmh table-result envelope into long-format rows.

    ips cells comma-PACK a (variable-length) resident/non-resident/total style
    breakdown with no thousands formatting -- exploded by position into
    ``breakdown_index``. pmh cells instead use thousands separators and carry a
    single value, read from the ``_SeqOrder`` companion. ``packed`` selects.
    """
    cols = year_columns(data.get("columns") or [])
    rows: list[dict] = []
    for rec in data.get("records") or []:
        office = rec.get("selectedOffice")
        origin = rec.get("selectedOrigin")
        for code, year in cols:
            pairs = explode(rec.get(code)) if packed else seqorder_value(rec, code)
            for breakdown_index, value in pairs:
                rows.append({
                    "office": office,
                    "origin": origin,
                    "indicator_id": indicator_id,
                    "indicator": indicator,
                    "report_type": report_type,
                    "year": year,
                    "breakdown_index": breakdown_index,
                    "value": value,
                })
    return rows
