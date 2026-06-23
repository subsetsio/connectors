"""Economist Big Mac Index connector.

Source: TheEconomist/big-mac-data on GitHub (CC BY 4.0). A small set of derived
CSV products served from stable raw.githubusercontent.com URLs on the `master`
branch. Tiny corpus (five files, all <1MB), so the fetch shape is the default:
stateless full re-pull per run — download each CSV in full, parse to a typed
parquet table, overwrite. No incremental query is supported by raw GitHub, and
none is needed at this size; revisions (the IMF refines GDP, late price fixes)
are picked up for free because we never trust a stored watermark.

The historical-source-data.csv file uses lone-CR (classic-Mac) line endings and
ISO-timestamp dates; both are normalized in the parser below.
"""
import csv
import datetime
import io

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

SLUG = "economist-big-mac-index"
BASE = "https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/"

# entity_id -> (relative file path, [(column, kind)]) where kind is one of
# "str" | "float" | "date". Column lists are the verified CSV headers.
CONFIG = {
    "big-mac-full-index": (
        "output-data/big-mac-full-index.csv",
        [
            ("date", "date"), ("iso_a3", "str"), ("currency_code", "str"),
            ("name", "str"), ("local_price", "float"), ("dollar_ex", "float"),
            ("dollar_price", "float"), ("USD_raw", "float"), ("EUR_raw", "float"),
            ("GBP_raw", "float"), ("JPY_raw", "float"), ("CNY_raw", "float"),
            ("GDP_bigmac", "float"), ("adj_price", "float"),
            ("USD_adjusted", "float"), ("EUR_adjusted", "float"),
            ("GBP_adjusted", "float"), ("JPY_adjusted", "float"),
            ("CNY_adjusted", "float"),
        ],
    ),
    "big-mac-raw-index": (
        "output-data/big-mac-raw-index.csv",
        [
            ("date", "date"), ("iso_a3", "str"), ("currency_code", "str"),
            ("name", "str"), ("local_price", "float"), ("dollar_ex", "float"),
            ("dollar_price", "float"), ("USD", "float"), ("EUR", "float"),
            ("GBP", "float"), ("JPY", "float"), ("CNY", "float"),
        ],
    ),
    "big-mac-adjusted-index": (
        "output-data/big-mac-adjusted-index.csv",
        [
            ("date", "date"), ("iso_a3", "str"), ("currency_code", "str"),
            ("name", "str"), ("local_price", "float"), ("dollar_ex", "float"),
            ("dollar_price", "float"), ("GDP_bigmac", "float"),
            ("adj_price", "float"), ("USD", "float"), ("EUR", "float"),
            ("GBP", "float"), ("JPY", "float"), ("CNY", "float"),
        ],
    ),
    "big-mac-source-data": (
        "source-data/big-mac-source-data-v2.csv",
        [
            ("name", "str"), ("iso_a3", "str"), ("currency_code", "str"),
            ("local_price", "float"), ("dollar_ex", "float"),
            ("GDP_dollar", "float"), ("GDP_local", "float"), ("date", "date"),
        ],
    ),
    "big-mac-historical-source-data": (
        "source-data/big-mac-historical-source-data.csv",
        [
            ("name", "str"), ("iso_a3", "str"), ("currency_code", "str"),
            ("local_price", "float"), ("dollar_ex", "float"), ("date", "date"),
        ],
    ),
}

_ARROW_TYPE = {"str": pa.string(), "float": pa.float64(), "date": pa.date32()}


def _entity_id(node_id: str) -> str:
    return node_id[len(SLUG) + 1:]


def _parse_cell(value: str, kind: str):
    if value is None or value == "":
        return None
    if kind == "str":
        return value
    if kind == "float":
        return float(value)
    if kind == "date":
        # handles both "2000-04-01" and "1986-09-01T00:00:00Z"
        return datetime.date.fromisoformat(value[:10])
    raise ValueError(f"unknown column kind: {kind}")


@transient_retry()
def _download_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = _entity_id(node_id)
    rel_path, columns = CONFIG[entity_id]

    text = _download_csv(BASE + rel_path)
    # Normalize lone-CR / CRLF line endings (historical file uses lone CR).
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    rows = list(csv.DictReader(io.StringIO(text)))

    schema = pa.schema([(name, _ARROW_TYPE[kind]) for name, kind in columns])
    arrays = [
        pa.array([_parse_cell(r.get(name), kind) for r in rows],
                 type=_ARROW_TYPE[kind])
        for name, kind in columns
    ]
    table = pa.Table.from_arrays(arrays, schema=schema)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in CONFIG
]

# Each subset is a thin parse-and-type pass over its own typed raw parquet:
# drop rows missing the (date, iso_a3) natural key, dedup defensively. Columns
# are already typed at the raw layer, so the transform is the correctness gate
# (it fails loudly / returns 0 rows if the upstream shape ever changes).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT DISTINCT *
            FROM "{s.id}"
            WHERE date IS NOT NULL AND iso_a3 IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
