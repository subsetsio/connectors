"""INEGI BISE CL_* reference code lists.

One CL_* code list per reference subset (indicators, topics, units,
frequencies, sources, geo_areas). One request each, materialised as a
(code, description) parquet. A single parametric `fetch_catalog` drives all
six from `_CL_BY_ASSET`.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _catalog_codes

# Maps a download spec id -> the CL_* code list it materialises.
_CL_BY_ASSET = {
    "inegi-indicators": "CL_INDICATOR",
    "inegi-topics": "CL_TOPIC",
    "inegi-units": "CL_UNIT",
    "inegi-frequencies": "CL_FREQ",
    "inegi-sources": "CL_SOURCE",
    "inegi-geo-areas": "CL_GEO_AREA",
}

_CATALOG_SCHEMA = pa.schema([
    ("code", pa.string()),
    ("description", pa.string()),
])


def fetch_catalog(node_id: str) -> None:
    """Materialise one CL_* code list as a (code, description) parquet."""
    cl_name = _CL_BY_ASSET[node_id]
    codes = _catalog_codes(cl_name)
    rows = [{"code": c.get("value"), "description": c.get("Description")} for c in codes]
    table = pa.Table.from_pylist(rows, schema=_CATALOG_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="inegi-indicators", fn=fetch_catalog, kind="download"),
    NodeSpec(id="inegi-topics", fn=fetch_catalog, kind="download"),
    NodeSpec(id="inegi-units", fn=fetch_catalog, kind="download"),
    NodeSpec(id="inegi-frequencies", fn=fetch_catalog, kind="download"),
    NodeSpec(id="inegi-sources", fn=fetch_catalog, kind="download"),
    NodeSpec(id="inegi-geo-areas", fn=fetch_catalog, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="inegi-indicators-transform",
        deps=["inegi-indicators"],
        sql='SELECT code AS indicator_id, description FROM "inegi-indicators"',
    ),
    SqlNodeSpec(
        id="inegi-topics-transform",
        deps=["inegi-topics"],
        sql='SELECT code AS topic_id, description AS topic_name FROM "inegi-topics"',
    ),
    SqlNodeSpec(
        id="inegi-units-transform",
        deps=["inegi-units"],
        sql='SELECT code AS unit_id, description AS unit_name FROM "inegi-units"',
    ),
    SqlNodeSpec(
        id="inegi-frequencies-transform",
        deps=["inegi-frequencies"],
        sql='SELECT code AS freq_id, description AS frequency_name FROM "inegi-frequencies"',
    ),
    SqlNodeSpec(
        id="inegi-sources-transform",
        deps=["inegi-sources"],
        sql='SELECT code AS source_id, description AS source_name FROM "inegi-sources"',
    ),
    SqlNodeSpec(
        id="inegi-geo-areas-transform",
        deps=["inegi-geo-areas"],
        sql='SELECT code AS geo_id, description AS geo_name FROM "inegi-geo-areas"',
    ),
]
