"""Bundesagentur fuer Arbeit — official "Statistik der Bundesagentur fuer Arbeit"
BIDS API (live since Dec 2025).

Each entity is one national statistical table fetched whole by a single GET
against the JSON path .../pc/v1/tableFetch/dia/<TableCode>. The response is a
flat list of row objects; each row is one (period, metric) cell:

    {"attributes": {"0": {"DESC": "Mai 2026", ...}}, "value": 2950460,
     "showValue": "2.950.460", "metricName": "Arbeitslose", ...}

Shape (1): stateless full re-pull. Every table returns its complete history in
one request (no pagination, no incremental filter, no auth), so each refresh
re-fetches the whole table and overwrites. Periods are German "Monat Jahr"
labels (monthly tables; annual tables use the same label form) — parsed here to
year/month/ISO-date so the SQL transform stays a thin cast.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, get, transient_retry, save_raw_parquet
from constants import ENTITY_IDS, TABLE_CODES

SLUG = "bundesagentur-f-r-arbeit"
BASE = "https://statistik-dr.arbeitsagentur.de/bifrontend/bids-api/pc/v1/tableFetch/dia/"

GERMAN_MONTHS = {
    "Januar": 1, "Februar": 2, "März": 3, "April": 4, "Mai": 5, "Juni": 6,
    "Juli": 7, "August": 8, "September": 9, "Oktober": 10, "November": 11,
    "Dezember": 12,
}

SCHEMA = pa.schema([
    ("metric", pa.string()),
    ("period_label", pa.string()),
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("date", pa.string()),     # ISO yyyy-mm-dd, first of month; null if unparseable
    ("value", pa.float64()),
])


@transient_retry()
def _fetch_table(code: str) -> list:
    resp = get(BASE + code, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _parse_period(label):
    """'Mai 2026' -> (2026, 5, '2026-05-01'). Returns (None, None, None) if the
    label is not a recognisable 'Monat Jahr'."""
    if not isinstance(label, str):
        return None, None, None
    parts = label.split()
    if len(parts) != 2:
        return None, None, None
    mon = GERMAN_MONTHS.get(parts[0])
    if mon is None or not parts[1].isdigit():
        return None, None, None
    yr = int(parts[1])
    return yr, mon, f"{yr:04d}-{mon:02d}-01"


def _to_float(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    return None


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity_id = node_id[len(SLUG) + 1:]   # strip 'bundesagentur-f-r-arbeit-'
    code = TABLE_CODES[entity_id]         # KeyError = bug (id not in union)

    rows = _fetch_table(code)
    metric, period_label, year, month, date, value = [], [], [], [], [], []
    for row in rows:
        attrs = row.get("attributes") or {}
        first = next(iter(attrs.values()), {}) if isinstance(attrs, dict) else {}
        label = first.get("DESC") if isinstance(first, dict) else None
        yr, mon, iso = _parse_period(label)
        metric.append(row.get("metricName"))
        period_label.append(label)
        year.append(yr)
        month.append(mon)
        date.append(iso)
        value.append(_to_float(row.get("value")))

    table = pa.table(
        {
            "metric": metric,
            "period_label": period_label,
            "year": year,
            "month": month,
            "date": date,
            "value": value,
        },
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
