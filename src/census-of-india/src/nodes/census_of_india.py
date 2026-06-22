"""Census of India — ORGI published census tables (A-series).

Each entity is one published census table (an `idno` prefix like PC11_A02)
materialized from one or more legacy Excel workbooks — one .xls/.xlsx per
geography (India / state / UT). The stable per-file download URLs were resolved
from the NADA catalog at collect time and baked into `constants.ENTITY_FILES`
(data, not logic). The corpus is static historical census data refreshed rarely,
so each fetch is a stateless full re-pull of the entity's member files.

The workbooks span ~200 heterogeneous layouts with multi-row merged headers and
no machine-readable schema, and DuckDB cannot read the legacy binary .xls, so
parsing + reshaping happens here in Python (`utils.excel_to_long`): every
workbook is melted to a uniform tidy-long shape — (region, dimensions, measure,
value) — and saved as drifty NDJSON. The SQL transform is then a thin typed
projection that publishes one Delta table per entity.
"""

from urllib.parse import unquote

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry

from constants import ENTITY_IDS, ENTITY_FILES
from utils import excel_to_long, install_ca

PREFIX = "census-of-india-"


@transient_retry()
def _download(url: str) -> bytes:
    # censusindia.gov.in is slow on the bulk files; generous read timeout.
    resp = get(url, timeout=(10.0, 240.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime hands us the spec id; it IS the asset name
    install_ca()     # complete the emSign chain in this subprocess's http client

    entity_id = node_id[len(PREFIX):].upper().replace("-", "_")
    meta = ENTITY_FILES[entity_id]
    census_year = int(meta["census_year"])
    table_code = meta["table_code"]

    rows = []
    misses = []
    for url in meta["urls"]:
        filename = unquote(url.rsplit("/", 1)[-1])
        long_rows = excel_to_long(_download(url), filename)
        if not long_rows:
            misses.append(filename)
            continue
        for r in long_rows:
            r["census_year"] = census_year
            r["table_code"] = table_code
            r["source_file"] = filename
        rows.extend(long_rows)

    if misses:
        print(f"[{node_id}] {len(misses)}/{len(meta['urls'])} member file(s) "
              f"parsed to 0 rows: {misses}")
    if not rows:
        raise RuntimeError(
            f"{node_id}: parsed 0 rows from {len(meta['urls'])} member file(s)"
        )
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


def _transform_sql(asset: str) -> str:
    return f'''
        SELECT
            CAST(census_year AS INTEGER) AS census_year,
            table_code,
            source_file,
            region,
            dimensions,
            measure,
            CAST(value AS DOUBLE) AS value
        FROM "{asset}"
        WHERE value IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
