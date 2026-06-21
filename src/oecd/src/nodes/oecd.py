"""OECD connector — node module.

Source: OECD SDMX 2.1 REST API (chosen mechanism `sdmx_21`, base
https://sdmx.oecd.org/public/rest/, no auth). Each rank-accepted dataflow is
fetched in full from its stable per-dataset SDMX-CSV data endpoint:

    https://sdmx.oecd.org/public/rest/data/{AGENCY},{DATAFLOW}/all?format=csv

The version segment is omitted so the server returns the latest published
version of each dataflow (robust to version churn between collect and run).
The collect entity id is "{agency}:{dataflow_id}"; both coordinates are
recovered by splitting on the first ':'.

Scope: rank accepts the flagship national-aggregate dataflows (GDP, prices,
labour, population, health, education, tax/government finance, trade, FDI,
productivity, social, environment, R&D). The huge downscaled / local-area /
regional / micro-data families (e.g. CFE.EDS regional cubes, CRS/CBCR activity
micro-data) are intentionally ranked below the publish threshold — they are tens
of millions of rows each and not the headline statistical product.

SDMX-CSV is tidy (one observation per row). The header is
`DATAFLOW,<dim1>,...,<dimN>,TIME_PERIOD,OBS_VALUE,<attrs...>` where the
dimension/attribute columns differ per dataflow (each has its own DSD). We drop
only the fixed `DATAFLOW` envelope column, rename TIME_PERIOD/OBS_VALUE to
time_period/value, coerce value to float, and pass every remaining column
through verbatim (lower-cased) — a uniform-per-dataset long row.

Fetch shape: stateless full re-pull (shape 1). The response is **streamed**
line-by-line straight into a gzipped NDJSON writer so even multi-million-row
tables never materialise the whole CSV in memory (the first attempt at this
connector OOM-killed the runner by loading a downscaled table via resp.text).
A discontinued/unmapped dataflow returns 404 → permanent per-entity skip (no raw
written; its transform finds no rows → that one node fails in isolation).

Rate limits: OECD enforces 429s without a documented ceiling; the retry
decorator's exponential backoff (429 is transient) finds the natural pace.
"""
import csv
import itertools
import json as _json


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_writer,
    transient_retry,
)

BASE = "https://sdmx.oecd.org/public/rest/data"

# Only DATAFLOW is a pure envelope column we drop; TIME_PERIOD/OBS_VALUE are
# renamed; everything else (dimensions + attributes) is kept as a column.
_DROP_COLS = {"DATAFLOW", "TIME_PERIOD", "OBS_VALUE"}


def _to_value(raw: str):
    raw = (raw or "").strip()
    if raw == "" or raw == ":":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


# Sentinel: dataflow not available (permanent skip), distinct from "wrote 0".
_SKIP_404 = object()


@transient_retry()
def _stream_to_ndjson(agency: str, dataflow: str, asset: str):
    url = f"{BASE}/{agency},{dataflow}/all?format=csv"
    client = get_client()
    with client.stream("GET", url, timeout=(10.0, 600.0)) as resp:
        if resp.status_code == 404:
            return _SKIP_404  # permanent: not available for this data request
        resp.raise_for_status()  # 5xx/429 -> transient retry; other 4xx -> raise

        reader = csv.reader(resp.iter_lines())
        try:
            header = next(reader)
        except StopIteration:
            return 0  # empty body
        cols = [h.strip() for h in header]
        col = {c: i for i, c in enumerate(cols)}
        tp_i = col.get("TIME_PERIOD")
        val_i = col.get("OBS_VALUE")
        if tp_i is None or val_i is None:
            raise AssertionError(
                f"{agency}:{dataflow}: SDMX-CSV missing TIME_PERIOD/OBS_VALUE; "
                f"header={cols}"
            )
        keep_idx = [(i, c.lower()) for i, c in enumerate(cols)
                    if c not in _DROP_COLS]

        n = 0
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
            for parts in reader:
                if not parts or len(parts) <= max(tp_i, val_i):
                    continue
                row = {name: parts[i] for i, name in keep_idx if i < len(parts)}
                row["time_period"] = parts[tp_i]
                row["value"] = _to_value(parts[val_i])
                fh.write(_json.dumps(row, ensure_ascii=False))
                fh.write("\n")
                n += 1
        return n


def fetch_one(node_id: str) -> None:
    asset = node_id  # spec id IS the asset name
    entity_id = _SPEC_TO_ENTITY[node_id]
    agency, _, dataflow = entity_id.partition(":")

    result = _stream_to_ndjson(agency, dataflow, asset)
    if result is _SKIP_404:
        print(f"[oecd] {entity_id}: 404 not available; skipping")
        return
    print(f"[oecd] {entity_id}: wrote {result} observations")


from constants import ENTITY_IDS

# spec id -> original collect entity id (recovers agency+dataflow, which are
# lost to lower-casing / '_'->'-' in the spec id).
_SPEC_TO_ENTITY = {
    f"oecd-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"oecd-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One thin SQL transform per dataflow: pass the tidy long rows through, keeping
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
