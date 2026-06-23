"""Bank of Jamaica (jm-boj) connector — download + transform.

Mechanism: per-dataset static Excel workbooks linked from the BOJ /statistics/
leaf pages (research mechanism `bulk_excel`). One download node per dataset
code in the entity union. Each fetch scrapes the dataset's leaf page for the
workbook href (the /wp-content/uploads/{YYYY}/{MM}/ path varies per file and
the file is overwritten in place, so URLs are NEVER constructed — only scraped),
downloads the workbook, and melts it into a uniform long table of
(date, subtable, series, value, frequency, unit) via `utils.parse_workbook`.

Strategy: stateless full re-pull. Each workbook is a small-to-medium long
time series re-fetched and overwritten every run; there is no incremental
filter on the source (research: "no incremental — full corpus per refresh")
and revisions are picked up for free. Excel parsing happens in the fetch fn
because the SQL transform can only read parquet — the transform is then a thin
type/clean pass that publishes one Delta table per dataset.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from constants import ENTITY_IDS
from utils import (
    http_get,
    leaf_for,
    resolve_workbook_url,
    parse_workbook,
)

_PREFIX = "jm-boj-"


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name to write
    code = node_id[len(_PREFIX):].upper()  # "jm-boj-fs.cb.00" -> "FS.CB.00"

    leaf_html = http_get(leaf_for(code)).text
    url = resolve_workbook_url(code, leaf_html)
    raw = http_get(url).content

    table = parse_workbook(code, raw, is_xlsx=url.lower().endswith("xlsx"))
    if table.num_rows == 0:
        # A standardized BOJ workbook always carries data; 0 rows means the
        # layout changed and the parser missed it — fail loudly, don't publish.
        raise RuntimeError(f"{code}: parsed 0 data rows from {url}")
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{_PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(date AS DATE)    AS date,
                subtable,
                series,
                CAST(value AS DOUBLE) AS value,
                frequency,
                unit
            FROM "{s.id}"
            WHERE value IS NOT NULL AND series IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
