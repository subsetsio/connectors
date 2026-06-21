"""Eurostat connector — node module.

Source: Eurostat SDMX 2.1 dissemination API (chosen mechanism `sdmx_21`,
agency ESTAT, no auth). Each rank-accepted dataflow is fetched in full from its
stable per-dataset SDMX-CSV endpoint:

    https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{CODE}/?format=SDMX-CSV

SDMX-CSV is tidy (one observation per row). The header is
`DATAFLOW,LAST UPDATE,<dim1>,...,<dimN>,TIME_PERIOD,OBS_VALUE,OBS_FLAG[,CONF_STATUS]`
where the dimension columns differ per dataflow (each has its own DSD). We strip
the fixed envelope columns, lower-case the remaining dimension columns, and emit
a uniform-per-dataset long row: {<dims...>, time_period, value, flag}. Raw is
NDJSON (heterogeneous dimension sets across datasets; stable within a dataset).

Fetch shape: stateless full re-pull (shape 1). The whole table is re-fetched and
overwritten every run — Eurostat has no per-observation incremental filter, and
re-pulling picks up revisions for free. A missing/discontinued dataset returns a
404 SOAP fault; that is a permanent per-entity skip (the asset is simply not
written and its transform finds no rows → that node fails in isolation).

Memory: raw is streamed to NDJSON (gzip) row-by-row so large detailed tables
(millions of observations) don't materialise a giant in-memory list.
"""
import csv
import io
import json as _json

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    transient_retry,
)

BASE = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"

# Fixed SDMX-CSV envelope columns — everything else in the header is a dimension.
_META_COLS = {
    "DATAFLOW",
    "LAST UPDATE",
    "LAST_UPDATE",
    "TIME_PERIOD",
    "OBS_VALUE",
    "OBS_FLAG",
    "CONF_STATUS",
    "OBS_STATUS",
}


@transient_retry()
def _fetch_csv(code: str) -> httpx.Response:
    url = f"{BASE}/{code}/?format=SDMX-CSV"
    resp = get(url, timeout=(10.0, 300.0))
    # 404 = dataset not available for dissemination: permanent, do not retry.
    if resp.status_code == 404:
        return resp
    resp.raise_for_status()
    return resp


def _to_value(raw: str):
    raw = (raw or "").strip()
    if raw == "" or raw == ":":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def fetch_one(node_id: str) -> None:
    asset = node_id  # spec id IS the asset name
    code = node_id[len("eurostat-"):].replace("-", "_").upper()

    resp = _fetch_csv(code)
    if resp.status_code == 404:
        # Discontinued / not disseminated: skip this entity cleanly. Its
        # transform will find no raw and that single node fails in isolation.
        print(f"[eurostat] {code}: 404 not available for dissemination; skipping")
        return

    reader = csv.reader(io.StringIO(resp.text))
    try:
        header = next(reader)
    except StopIteration:
        print(f"[eurostat] {code}: empty response; skipping")
        return

    # Indices of the columns we care about.
    dim_idx = [(i, h.strip().lower()) for i, h in enumerate(header) if h.strip() not in _META_COLS]
    col = {h.strip(): i for i, h in enumerate(header)}
    tp_i = col.get("TIME_PERIOD")
    val_i = col.get("OBS_VALUE")
    flag_i = col.get("OBS_FLAG")
    if tp_i is None or val_i is None:
        raise AssertionError(f"{code}: SDMX-CSV missing TIME_PERIOD/OBS_VALUE; header={header}")

    n = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for parts in reader:
            if not parts or len(parts) <= max(tp_i, val_i):
                continue
            row = {name: parts[i] for i, name in dim_idx}
            row["time_period"] = parts[tp_i]
            row["value"] = _to_value(parts[val_i])
            row["flag"] = parts[flag_i].strip() if (flag_i is not None and flag_i < len(parts)) else ""
            fh.write(_json.dumps(row, ensure_ascii=False))
            fh.write("\n")
            n += 1
    print(f"[eurostat] {code}: wrote {n} observations")


from constants import ENTITY_IDS

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"eurostat-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One thin SQL transform per dataset: pass the tidy long rows through, keeping
# only real observations. Each dataflow publishes its own dimension columns
# (distinct DSD), so a generic SELECT * is the correct uniform shape.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}" WHERE value IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
