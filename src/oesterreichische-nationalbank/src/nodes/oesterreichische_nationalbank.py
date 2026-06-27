"""Oesterreichische Nationalbank (OeNB) connector.

OeNB exposes a proprietary, open XML web service ("ISA Data Service", NOT SDMX).
Two published subsets:

  - positions : the indicator-position catalog (one row per pos code: pos, title,
                hierid, node name). A small reference table.
  - values    : long-format observations across every position. One row per
                (pos, dimension-combination, frequency, period).

Both are built by walking the category tree (content endpoint) to discover the
positions, then -- for values -- fetching the data endpoint per node. The data
endpoint REQUIRES the matching hierid alongside pos (probing showed pos without
its node, or with the wrong node, returns zero dataSets), so positions are always
fetched grouped by their node. Multiple pos= are allowed per request, so we chunk.
"""

import xml.etree.ElementTree as ET

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://www.oenb.at/isadataservice"
LANG = "EN"

# Positions per data request. The endpoint accepts many pos= in one call, but
# each pos fans out across every dimension combination x frequency x its full
# history -- a handful of positions can be >100k observations -- so keep the
# batch small to bound per-request response size and memory. Each request's rows
# are written as their own parquet batch file.
POS_PER_REQUEST = 10

SLUG = "oesterreichische-nationalbank"

VALUES_SCHEMA = pa.schema(
    [
        ("pos", pa.string()),
        ("pos_title", pa.string()),
        ("hierid", pa.string()),
        ("freq", pa.string()),
        ("attr1", pa.string()),
        ("attr1_dim", pa.string()),
        ("attr2", pa.string()),
        ("attr2_dim", pa.string()),
        ("attr3", pa.string()),
        ("attr3_dim", pa.string()),
        ("attr4", pa.string()),
        ("attr4_dim", pa.string()),
        ("unit_mult", pa.string()),
        ("unit_text", pa.string()),
        ("period", pa.string()),
        ("value", pa.float64()),
    ]
)

POSITIONS_SCHEMA = pa.schema(
    [
        ("pos", pa.string()),
        ("title", pa.string()),
        ("hierid", pa.string()),
        ("node_name", pa.string()),
    ]
)


# --- HTTP -----------------------------------------------------------------------

@transient_retry()
def _get_xml(path: str, params) -> bytes:
    resp = get(f"{BASE}/{path}", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


# --- catalog walk ---------------------------------------------------------------

def _category_nodes() -> list[tuple[str, str]]:
    """The whole hierarchy in one `content` call -> [(hierid, node_name)]."""
    root = ET.fromstring(_get_xml("content", [("lang", LANG)]))
    nodes = []
    for el in root.iterfind(".//element"):
        nid = el.get("id")
        name = (el.findtext("text") or "").strip()
        if nid:
            nodes.append((nid, name))
    return nodes


def _positions_for_node(hierid: str) -> list[tuple[str, str]]:
    """`content?hierid=` -> [(pos, title)] for a leaf node (empty for branches)."""
    root = ET.fromstring(_get_xml("content", [("lang", LANG), ("hierid", hierid)]))
    out = []
    for p in root.iterfind(".//position"):
        pid = p.get("id")
        title = (p.findtext("text") or "").strip()
        if pid:
            out.append((pid, title))
    return out


def _chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def _parse_float(raw):
    if raw in (None, "", ".", "NaN"):
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


# --- download: positions catalog ------------------------------------------------

def fetch_positions(node_id: str) -> None:
    asset = node_id
    rows = {
        "pos": [],
        "title": [],
        "hierid": [],
        "node_name": [],
    }
    for hierid, node_name in _category_nodes():
        for pos, title in _positions_for_node(hierid):
            rows["pos"].append(pos)
            rows["title"].append(title)
            rows["hierid"].append(hierid)
            rows["node_name"].append(node_name)
    if not rows["pos"]:
        raise AssertionError("positions catalog walk produced 0 positions")
    table = pa.table(rows, schema=POSITIONS_SCHEMA)
    save_raw_parquet(table, asset)


# --- download: observations -----------------------------------------------------

def _data_rows_for_chunk(hierid: str, chunk: list[str]) -> dict:
    cols = {f.name: [] for f in VALUES_SCHEMA}
    params = [("lang", LANG), ("hierid", hierid)] + [("pos", p) for p in chunk]
    root = ET.fromstring(_get_xml("data", params))
    for ds in root.iter("dataSet"):
        a = ds.attrib
        vals = ds.find("values")
        if vals is None:
            continue
        for o in vals.findall("obs"):
            cols["pos"].append(a.get("pos"))
            cols["pos_title"].append(a.get("posTitle"))
            cols["hierid"].append(hierid)
            cols["freq"].append(a.get("freq"))
            cols["attr1"].append(a.get("attr1"))
            cols["attr1_dim"].append(a.get("attr1Dim"))
            cols["attr2"].append(a.get("attr2"))
            cols["attr2_dim"].append(a.get("attr2Dim"))
            cols["attr3"].append(a.get("attr3"))
            cols["attr3_dim"].append(a.get("attr3Dim"))
            cols["attr4"].append(a.get("attr4"))
            cols["attr4_dim"].append(a.get("attr4Dim"))
            cols["unit_mult"].append(a.get("unitMult"))
            cols["unit_text"].append(a.get("unitText"))
            cols["period"].append(o.get("periode"))
            cols["value"].append(_parse_float(o.get("value")))
    return cols


def fetch_values(node_id: str) -> None:
    # One parquet batch file per (node, position-chunk):
    # f"{node_id}-{hierid}-{chunk_index}". Each pos fans out into a large number
    # of observations, so writing per chunk keeps peak memory bounded. The
    # transform globs "{node_id}-*" to union every batch.
    asset = node_id
    nodes = _category_nodes()
    wrote_any = False
    for hierid, _name in nodes:
        positions = [pos for pos, _t in _positions_for_node(hierid)]
        if not positions:
            continue  # branch node, no series
        for ci, chunk in enumerate(_chunks(positions, POS_PER_REQUEST)):
            cols = _data_rows_for_chunk(hierid, chunk)
            if not cols["pos"]:
                continue  # this chunk yielded no observations
            table = pa.table(cols, schema=VALUES_SCHEMA)
            save_raw_parquet(table, f"{asset}-{hierid}-{ci}")
            wrote_any = True
    if not wrote_any:
        raise AssertionError("values walk produced no observations for any node")


# --- specs ----------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-positions", fn=fetch_positions, kind="download"),
    NodeSpec(id=f"{SLUG}-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-positions-transform",
        deps=[f"{SLUG}-positions"],
        sql=f'''
            SELECT
                pos,
                title,
                hierid,
                node_name
            FROM "{SLUG}-positions"
            WHERE pos IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{SLUG}-values-transform",
        deps=[f"{SLUG}-values"],
        sql=f'''
            SELECT
                pos,
                pos_title,
                hierid,
                freq,
                attr1, attr1_dim,
                attr2, attr2_dim,
                attr3, attr3_dim,
                attr4, attr4_dim,
                TRY_CAST(unit_mult AS INTEGER) AS unit_mult,
                unit_text,
                period,
                TRY_CAST(substr(period, 1, 4) AS INTEGER) AS year,
                CAST(value AS DOUBLE) AS value
            FROM "{SLUG}-values"
            WHERE value IS NOT NULL
        ''',
    ),
]
