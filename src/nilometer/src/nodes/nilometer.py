"""Roda Nilometer — annual minimum Nile water levels (A.D. 622-1284).

A single famous historical time series: the annual MINIMUM (low-water) gauge
reading of the Nile at the Roda Nilometer near Cairo, one value per year for
622-1284 (663 yearly observations). Compiled by Toussoun (1925) and distributed
as Beran's long-memory dataset.

The one verified mechanism is a single ~2.5 KB plain-text file from the cran org
mirror of the CRAN `longmemo` package. The payload is an R `ts()` literal:

    NileMin <- ts(1000 +
    c(157,88,169,169,-16, ... ,108,97), start=622)

We parse the comma-separated integer offsets inside `c(...)`, add the literal
`1000` offset, and assign year = 622 + index. This is an immutable historical
artefact, so the fetch is a stateless full re-pull every run (trivially cheap —
one request, 663 rows). Freshness gating is the maintain step's concern.
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

SOURCE_URL = "https://raw.githubusercontent.com/cran/longmemo/master/data/NileMin.R"
START_YEAR = 622  # `start=622` in the R ts() literal; documented span is 622-1284
LEVEL_OFFSET = 1000  # the literal `1000 +` prefix the R expression adds to each value

SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("min_level", pa.int32()),
])


@transient_retry()  # 6 attempts, exponential backoff over transient net + 429 + 5xx
def _fetch_source_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _parse_nilemin(text: str) -> list[dict]:
    """Extract (year, min_level) rows from the R `ts(1000 + c(...))` literal."""
    m = re.search(r"c\((.*?)\)", text, re.DOTALL)
    if not m:
        # Bug / source-format change — don't retry, surface loudly.
        raise AssertionError("NileMin.R: could not locate the c(...) value vector")
    offsets = [int(tok) for tok in re.findall(r"-?\d+", m.group(1))]
    if not offsets:
        raise AssertionError("NileMin.R: c(...) parsed to zero values")
    return [
        {"year": START_YEAR + i, "min_level": LEVEL_OFFSET + off}
        for i, off in enumerate(offsets)
    ]


def fetch_minima(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    text = _fetch_source_text(SOURCE_URL)
    rows = _parse_nilemin(text)
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="nilometer-roda-nilometer-annual-minima",
        fn=fetch_minima,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(year AS INTEGER)      AS year,
                CAST(min_level AS INTEGER) AS min_level
            FROM "{s.id}"
            WHERE year IS NOT NULL AND min_level IS NOT NULL
            ORDER BY year
        ''',
    )
    for s in DOWNLOAD_SPECS
]
