"""World Bank — values (firehose; supervisor-bounded, resumable via watermark).

Long-format observations (indicator x country x year). The full corpus is
~29.5k indicators x ~300 countries x ~65 years, far too large to pull in one
run, so it walks the indicator universe (in id-sorted order) and writes one
parquet batch per chunk. State holds a watermark = the last indicator id
completed; if the supervisor interrupts the node before the sweep finishes, the
next run resumes from that watermark. The data API exposes no modified-since
filter, so values are re-derived by walking the indicator catalog rather than
by timestamp.
"""
import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet, load_state, save_state
from utils import _IndicatorUnavailable, _fetch_all_pages, _nested, _to_float, _indicator_rows

STATE_VERSION = 1

# How many indicators accumulate into one parquet batch file — tuned so each batch
# lands at a moderate size. There is no per-run indicator/time cap: the loop sweeps
# the whole indicator universe and the supervisor interrupts the node (→ pending →
# continuation) if the run nears its CI wall-clock; per-batch raw+state writes make
# that interrupt safe to resume.
INDICATORS_PER_BATCH = 50

_VALUE_SCHEMA = pa.schema([
    ("indicator_code", pa.string()),
    ("indicator_name", pa.string()),
    ("source_id", pa.string()),
    ("country_id", pa.string()),
    ("country_iso3", pa.string()),
    ("country_name", pa.string()),
    ("date", pa.string()),
    ("value", pa.float64()),
    ("unit", pa.string()),
    ("obs_status", pa.string()),
])


def _fetch_indicator_observations(indicator_id: str, source_id: str):
    """Long-format observations for one indicator across all countries/years."""
    params = {}
    if source_id:
        params["source"] = source_id
    try:
        records = _fetch_all_pages(
            f"country/all/indicator/{indicator_id}", params, per_page=20000
        )
    except _IndicatorUnavailable:
        # Deleted/archived/non-queryable indicator (200 + message envelope).
        return []
    except httpx.HTTPStatusError as exc:
        # A 400/404 that survives the full retry budget means this particular
        # indicator/source pair is not queryable via the data endpoint (a known
        # quirk across the ~29.5k-indicator universe). Skip it rather than sink
        # the entire values sweep on one bad entry.
        if exc.response.status_code in (400, 404):
            return []
        raise
    out = []
    for r in records:
        out.append({
            "indicator_code": _nested(r, "indicator", "id") or indicator_id,
            "indicator_name": _nested(r, "indicator", "value"),
            "source_id": source_id,
            "country_id": _nested(r, "country", "id"),
            "country_iso3": (r.get("countryiso3code") or "").strip(),
            "country_name": _nested(r, "country", "value"),
            "date": (r.get("date") or "").strip(),
            "value": _to_float(r.get("value")),
            "unit": (r.get("unit") or "").strip(),
            "obs_status": (r.get("obs_status") or "").strip(),
        })
    return out


def fetch_values(node_id: str) -> None:
    state_key = node_id  # "world-bank-values"
    state = load_state(state_key)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "watermark": ""}
    watermark = state.get("watermark", "")

    # Discover the full indicator universe (id-sorted) every run. The list is
    # cheap (~2 pages) and being recomputed makes new indicators show up at the
    # tail automatically.
    catalog = sorted(
        ((r["id"], r["source_id"]) for r in _indicator_rows() if r.get("id")),
        key=lambda t: t[0],
    )
    total = len(catalog)
    start_idx = next((i for i, (iid, _) in enumerate(catalog) if iid > watermark), total)

    idx = start_idx
    while idx < total:
        chunk = catalog[idx:idx + INDICATORS_PER_BATCH]
        batch_rows = []
        for indicator_id, source_id in chunk:
            batch_rows.extend(_fetch_indicator_observations(indicator_id, source_id))

        batch_key = f"{idx:06d}-{idx + len(chunk) - 1:06d}"
        if batch_rows:
            table = pa.Table.from_pylist(batch_rows, schema=_VALUE_SCHEMA)
            save_raw_parquet(table, f"{node_id}-{batch_key}")  # write raw FIRST

        # Advance watermark to the last indicator id in this chunk, then persist.
        state = {"schema_version": STATE_VERSION, "watermark": chunk[-1][0]}
        save_state(state_key, state)

        idx += len(chunk)


DOWNLOAD_SPECS = [
    NodeSpec(id="world-bank-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="world-bank-values-transform",
        deps=["world-bank-values"],
        sql='''
            SELECT
                indicator_code,
                indicator_name,
                source_id,
                country_id,
                NULLIF(country_iso3, '')    AS country_iso3,
                country_name,
                TRY_CAST(date AS INTEGER)   AS year,
                date                        AS period,
                CAST(value AS DOUBLE)       AS value,
                NULLIF(obs_status, '')      AS obs_status
            FROM (
                SELECT *,
                    row_number() OVER (
                        PARTITION BY indicator_code, country_id, date
                        ORDER BY value DESC NULLS LAST
                    ) AS _rn
                FROM "world-bank-values"
                WHERE value IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
