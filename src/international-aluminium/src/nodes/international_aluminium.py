"""International Aluminium Institute (IAI) statistics connector.

Source: the "alvis" backend that powers the interactive charts on
international-aluminium.org/statistics/*. One GET per publication returns that
publication's COMPLETE time series in a single JSON response (no pagination):

    GET https://alvis.international-aluminium.org/api/publication/?publication=<slug>
    header  X-AUTH-TOKEN: <public token embedded in the stats page HTML>

Each response carries `data.publication.charts` with:
  - `columns` : the dimension shown across columns (regions / technologies /
                processes / accident-severity measures ...), id + name.
  - `rows`    : the dimension shown down rows (measures / series), id + name +
                optional `publicationRowGroup`.
  - `data`    : a list of periods; each period has `period` (name/from/to) and a
                nested {row_id: {col_id: {value}}} cell matrix.

We pull the full corpus every run (shape 1, stateless full re-pull): the whole
source is ~13 small datasets / a few MB, the API has no incremental filter, and
re-pulling picks up revisions for free. No state, no watermark.

Each publication is flattened to one long-format Delta table:
  (period_name, period_start, period_end, series_group, series, category, value)
one row per (period x declared-row x declared-column) cell that has a value.

Stray column/row ids that appear in the cell matrix but NOT in the declared
`columns`/`rows` metadata (legacy/hidden series) are dropped — we only publish
the source's own declared dimensions.
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "international-aluminium"
PREFIX = f"{SLUG}-"

API_URL = "https://alvis.international-aluminium.org/api/publication/"
# Public token hard-coded in the international-aluminium.org stats page HTML
# (window.ALVIS_API_TOKEN). Not a per-user credential; the API 401s without it.
API_TOKEN = (
    "VqJoChv3cGZei872eHVKUL4kdbk3CG2qw5RUpq8eV4VmMCbCJxncfzOyCo3nknz"
    "59qoWzPjVsPFffSULSWceeWAuywurxWiRVXdkqADVfKSvItSkOstAcU8yoiL6Hmr6"
)

# Long-format schema, identical for every publication. value is the only metric;
# its unit varies by publication (kt, kWh/t, t CO2e/t, ...) and is documented in
# the publication's own definition text, so we keep it a bare DOUBLE.
SCHEMA = pa.schema(
    [
        ("period_name", pa.string()),
        ("period_start", pa.date32()),
        ("period_end", pa.date32()),
        ("series_group", pa.string()),
        ("series", pa.string()),
        ("category", pa.string()),
        ("value", pa.float64()),
    ]
)


@transient_retry()
def _fetch(slug: str) -> dict:
    resp = get(
        API_URL,
        params={"publication": slug},
        headers={"X-AUTH-TOKEN": API_TOKEN, "Accept": "application/json"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("error"):
        raise AssertionError(f"{slug}: API returned error flag: {payload!r}")
    return payload


def _to_date(iso: str):
    # period.from / period.to look like "1973-01-01T00:00:00+00:00"; take the
    # calendar date portion.
    from datetime import date

    return date.fromisoformat(iso[:10])


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    slug = node_id[len(PREFIX):]

    charts = _fetch(slug)["data"]["publication"]["charts"]

    row_meta = {
        int(r["id"]): (r.get("publicationRowGroup"), r["name"])
        for r in charts["rows"]
    }
    col_meta = {int(c["id"]): c["name"] for c in charts["columns"]}

    period_names, starts, ends = [], [], []
    groups, series, categories, values = [], [], [], []

    for period in charts["data"]:
        p = period["period"]
        pname = p.get("name")
        pstart = _to_date(p["from"])
        pend = _to_date(p["to"])
        for row_id, cells in period["data"].items():
            rid = int(row_id)
            if rid not in row_meta:
                continue  # stray / undeclared row
            grp, sname = row_meta[rid]
            for col_id, cell in cells.items():
                cid = int(col_id)
                if cid not in col_meta:
                    continue  # stray / undeclared column
                if cell is None:
                    continue
                val = cell.get("value")
                if val is None:
                    continue
                period_names.append(pname)
                starts.append(pstart)
                ends.append(pend)
                groups.append(grp)
                series.append(sname)
                categories.append(col_meta[cid])
                values.append(float(val))

    table = pa.Table.from_pydict(
        {
            "period_name": period_names,
            "period_start": starts,
            "period_end": ends,
            "series_group": groups,
            "series": series,
            "category": categories,
            "value": values,
        },
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per publication. The raw is already clean long
# format; the transform is a thin type-and-project pass (and the correctness
# gate — a wrong raw shape fails the cast here, 0 rows fails the node).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(period_start AS DATE) AS period_start,
                CAST(period_end   AS DATE) AS period_end,
                period_name,
                series_group,
                series,
                category,
                CAST(value AS DOUBLE)      AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
