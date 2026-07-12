"""PYPL popularity indices.

PYPL publishes four monthly "popularity" indices, each derived from Google
Trends tutorial-search share: PYPL (programming languages), TOPDB (databases),
Top IDE, and TOP ODE (online development environments). Each index is published
as a JavaScript file per country at
``https://raw.githubusercontent.com/pypl/pypl.github.io/master/<INDEX>/<COUNTRY>.js``
containing ``graphData = [ ['Date', e1, e2, ...], [new Date(y,m,1), v1, ...], ... ]``.

One download node per index fetches all six country files (All, US, GB, DE, FR,
IN), parses the JS array literals, and writes one long-format parquet
(date, country, entity, share). The whole corpus is ~1-2 MB across 24 small
static files, so this is a stateless full re-pull every run — no watermark.
"""

import re
from datetime import date

import pyarrow as pa
from subsets_utils import NodeSpec, get, save_raw_parquet, transient_retry

RAW_URL = "https://raw.githubusercontent.com/pypl/pypl.github.io/master/{dir}/{country}.js"
COUNTRIES = ["All", "US", "GB", "DE", "FR", "IN"]

# entity_id (from the entity union) -> source directory + the published entity
# column name for that index.
INDEX_CONFIG = {
    "pypl-languages": {"dir": "PYPL", "col": "language"},
    "topdb-databases": {"dir": "DB", "col": "database"},
    "top-ide": {"dir": "IDE", "col": "ide"},
    "top-ode": {"dir": "ODE", "col": "online_dev_environment"},
}

SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("country", pa.string()),
    ("entity", pa.string()),
    ("share", pa.float64()),
])


@transient_retry()
def _fetch_js(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _parse(js: str):
    """Parse a PYPL .js file into (entity_names, [(year, month0, [values]), ...])."""
    start = js.index("['Date'")
    end = js.index("]", start)
    header = js[start:end]
    entities = [n for n in re.findall(r"'([^']*)'", header) if n != "Date"]

    rows = []
    for y, m, _d, rest in re.findall(r"\[new Date\((\d+),(\d+),(\d+)\),([^\]]*)\]", js):
        values = [float(x) for x in rest.split(",")]
        if len(values) != len(entities):
            raise AssertionError(
                f"row {y}-{int(m)+1}: {len(values)} values vs {len(entities)} entities"
            )
        rows.append((int(y), int(m), values))
    return entities, rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("pypl-"):]
    cfg = INDEX_CONFIG[entity_id]

    # Dedupe on (date, country, entity): a handful of months near 2005 are
    # duplicated in source; keep the last occurrence.
    merged: dict[tuple, float] = {}
    for country in COUNTRIES:
        js = _fetch_js(RAW_URL.format(dir=cfg["dir"], country=country))
        entities, rows = _parse(js)
        for year, month0, values in rows:
            d = date(year, month0 + 1, 1)
            for name, share in zip(entities, values):
                merged[(d, country, name)] = share

    keys = sorted(merged)
    table = pa.table(
        {
            "date": pa.array([k[0] for k in keys], pa.date32()),
            "country": pa.array([k[1] for k in keys], pa.string()),
            "entity": pa.array([k[2] for k in keys], pa.string()),
            "share": pa.array([merged[k] for k in keys], pa.float64()),
        },
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"pypl-{eid}", fn=fetch_one, kind="download")
    for eid in INDEX_CONFIG
]
