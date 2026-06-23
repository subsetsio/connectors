"""DG ECFIN Business and Consumer Surveys (BCS) connector.

One download per BCS dataflow (ECFIN REDISSTAT SDMX 2.1), fetched as SDMX-CSV
and normalized to a tidy long-format row stream. Each dataflow's dimension
columns differ (industry/services/consumer vs the investment surveys), so raw
is saved as NDJSON and the transform is a thin per-dataflow type/clean pass.
"""

import csv
import io

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry
from constants import ENTITY_IDS

SLUG = "dg-ecfin-business-and-consumer-surveys"
BASE = "https://webgate.ec.europa.eu/ecfin/redisstat/api/dissemination/sdmx/2.1/data"
# SDMX-CSV must be requested via the Accept header — the ?format=csvdata param 406s.
CSV_ACCEPT = "application/vnd.sdmx.data+csv;version=1.0.0"

# Source columns we rename/replace; everything else (the dataflow's dimension
# columns) is carried through verbatim, lower-cased.
_DROP = {"dataflow", "time_period", "obs_value"}
_RENAME = {"last update": "last_update", "ref_area": "ref_area"}


def _dataflow_id(node_id: str) -> str:
    """Recover the SDMX dataflow id from the spec id."""
    return node_id[len(SLUG) + 1:].upper().replace("-", "_")


def _period_to_date(period: str) -> str | None:
    """Normalize an SDMX TIME_PERIOD to the ISO date of the period start.

    Handles annual (2021), monthly (2016-05) and quarterly (2025-Q1).
    """
    period = period.strip()
    if not period:
        return None
    if "-Q" in period:
        year, q = period.split("-Q")
        month = (int(q) - 1) * 3 + 1
        return f"{int(year):04d}-{month:02d}-01"
    parts = period.split("-")
    if len(parts) == 1:  # annual
        return f"{int(parts[0]):04d}-01-01"
    if len(parts) >= 2:  # monthly YYYY-MM
        return f"{int(parts[0]):04d}-{int(parts[1]):02d}-01"
    return None


@transient_retry()
def _fetch_csv(dataflow: str) -> str:
    resp = get(f"{BASE}/{dataflow}", headers={"Accept": CSV_ACCEPT}, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text


def fetch_one(node_id: str) -> None:
    dataflow = _dataflow_id(node_id)
    text = _fetch_csv(dataflow)
    reader = csv.DictReader(io.StringIO(text))
    fields = [f for f in (reader.fieldnames or []) if f]  # drop trailing-comma None column

    rows = []
    for rec in reader:
        raw_value = (rec.get("OBS_VALUE") or "").strip()
        if raw_value == "":
            continue  # no observation
        try:
            value = float(raw_value)
        except ValueError:
            continue
        out = {"date": _period_to_date(rec.get("TIME_PERIOD", "")), "value": value}
        for f in fields:
            key = f.strip().lower()
            if key in _DROP:
                continue
            key = _RENAME.get(key, key)
            out[key] = (rec.get(f) or "").strip() or None
        if out["date"] is None:
            continue
        rows.append(out)

    if not rows:
        raise AssertionError(f"{dataflow}: parsed zero observations from SDMX-CSV")

    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Thin parse-and-type pass per dataflow. Columns vary across dataflows, so we
# pass them through with EXCLUDE and only retype the two normalized columns.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(date AS DATE)     AS date,
                * EXCLUDE (date, value),
                CAST(value AS DOUBLE)  AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
