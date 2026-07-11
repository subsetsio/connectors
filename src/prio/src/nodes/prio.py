"""PRIO (Peace Research Institute Oslo) connector.

No machine-readable catalog API exists (the prio.org/data listing is a Blazor
SPA over SignalR). Each dataset has a server-rendered page at /data/{id} whose
raw HTML carries direct cdn.cloud.prio.org/files/<uuid>/<filename> download
links. Strategy (full re-pull every run — the corpus is ~19 small/medium files
that re-fetch in a few minutes):

  1. GET the dataset page, regex out the cdn download links.
  2. Resolve the primary data file for this dataset from RESOLVE (the newest
     version's tabular file — academic datasets ship heterogeneous formats:
     csv / xls / xlsx / dta / sav, many bundled inside a per-dataset .zip with
     a codebook PDF and sometimes shapefiles).
  3. Download it, unzip + select the data member if needed, parse to a pandas
     DataFrame, sanitize columns, and write parquet raw.

PRIO-GRID (entity 40) ships its panel already as parquet inside the release
zip; that member is 36M rows, so it is stream-copied row-group by row-group
rather than materialized in memory.

There is no incremental query support anywhere on the source, so each refresh
re-fetches the full corpus and overwrites. PRIO bumps a dataset's version and
adds a new UUID file while keeping older versions linked; RESOLVE matches the
newest version's filename so the connector tracks updates automatically.
"""

import io
import os
import re
import tempfile
import urllib.parse

import httpx

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    raw_parquet_writer,
    transient_retry,
)

PAGE_URL = "https://www.prio.org/data/{id}"
CDN = "https://cdn.cloud.prio.org/files/{uuid}/{filename}"
EXCEL_HEADER_ROWS = {
    "14": 1,
    "34": 4,
}

# Authoritative entity union (rank-accepted, >= publish threshold).
from constants import ENTITY_IDS

# Per-dataset resolver: page_id -> (file_substr, file_ext, member_substr|None).
# file_substr + file_ext select the primary download link on the page (newest
# version); member_substr (for zips) selects the tabular member inside.
# Derived by probing every dataset's real download — see dev/ scripts.
RESOLVE = {
    "1":  ("battle deaths dataset", "xls",  None),
    "3":  ("annual onset",          "dta",  None),
    "4":  ("armed conflict dataset", "zip", "Main Conflict Table.xls"),
    "5":  ("conflictsite",          "xls",  None),
    "6":  ("usd 20 data",           "zip",  "events.xlsx"),
    "7":  ("acled",                 "zip",  "AcledEvents.xls"),
    "8":  ("geo-svac",              "zip",  "geosvac.csv"),
    "10": ("diadata data",          "zip",  "DIADATA Excel file.xls"),
    "11": ("petrodata v12 data",    "zip",  "Petrodata_Onshore_V1.2.xlsx"),
    "14": ("boundary length dataset", "xls", None),
    "16": ("witches brew dataset",  "sav",  None),
    "18": ("mirps data annual",      "dta",  None),
    "20": ("polyarchy v2 data",     "zip",  "polyarchy v2 dataset.csv"),
    "23": ("natresconfl",           "dta",  None),
    "26": ("waricc dataset",         "xlsx", None),
    "28": ("institutional variance dataset", "dta", None),
    "29": ("religious cleavages dataset", "dta", None),
    "30": ("location of armed conflict onset dataset", "xlsx", None),
    "31": ("conflictrecurrencedatabase", "csv", None),
    "32": ("usd 30 dataset",        "zip",  "events.xlsx"),
    "34": ("pfos mapping dataset",  "xlsx", None),
    "35": ("area database data",    "csv",  None),
    "36": ("shdi-sgdi-total",       "csv",  None),
    "37": ("gdl-corruptiondata",    "csv",  None),
    "38": ("gdl codes",             "xlsx", None),
    "39": ("omg_stata",             "zip",  "omg.dta"),
    "40": ("3_0_1",                 "zip",  "pg_timevarying.parquet"),
}


@transient_retry()
def _http_get(url: str) -> httpx.Response:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp


def _page_links(page_id: str):
    """Return [(uuid, filename), ...] of cdn download files on /data/{id},
    in page order, deduped."""
    html = _http_get(PAGE_URL.format(id=page_id)).text
    seen, out = set(), []
    for m in re.finditer(
        r'cdn\.cloud\.prio\.org/files/([0-9a-f-]+)/([^"?\\]+)', html
    ):
        uuid, fname = m.group(1), urllib.parse.unquote(m.group(2))
        if (uuid, fname) in seen:
            continue
        seen.add((uuid, fname))
        out.append((uuid, fname))
    return out


def _resolve_link(page_id: str, substr: str, ext: str):
    """Pick the primary download link matching substr + extension (first =
    newest version on the page)."""
    for uuid, fname in _page_links(page_id):
        low = fname.lower()
        if substr in low and low.endswith("." + ext):
            return uuid, fname
    raise RuntimeError(
        f"data/{page_id}: no download link matching '{substr}'.{ext}"
    )


def _zip_member(data: bytes, member_substr: str):
    """Return (member_name, member_bytes) for the data member of a zip,
    skipping AppleDouble (._*) and __MACOSX entries."""
    import zipfile

    zf = zipfile.ZipFile(io.BytesIO(data))
    members = [
        m for m in zf.namelist()
        if not m.endswith("/")
        and not m.split("/")[-1].startswith("._")
        and "__MACOSX" not in m
    ]
    exact = [m for m in members if m.split("/")[-1] == member_substr]
    fuzzy = [m for m in members if member_substr.lower() in m.lower()]
    hit = (exact or fuzzy)
    if not hit:
        raise RuntimeError(
            f"zip member '{member_substr}' not found; have {members[:12]}"
        )
    name = hit[0]
    return name, zf.read(name)


def _read_dataframe(data: bytes, ext: str, page_id: str | None = None):
    import pandas as pd

    header = EXCEL_HEADER_ROWS.get(page_id, 0)
    if ext == "csv":
        last = None
        for enc in ("utf-8", "latin-1"):
            try:
                df = pd.read_csv(io.BytesIO(data), encoding=enc, low_memory=False)
                if df.shape[1] == 1:  # likely a semicolon-delimited file
                    df = pd.read_csv(
                        io.BytesIO(data), encoding=enc, sep=";", low_memory=False
                    )
                return df
            except Exception as e:  # try next encoding
                last = e
        raise RuntimeError(f"csv parse failed: {last}")
    if ext == "xlsx":
        return pd.read_excel(io.BytesIO(data), engine="openpyxl", header=header)
    if ext == "xls":
        return pd.read_excel(io.BytesIO(data), engine="xlrd", header=header)
    if ext == "dta":
        return pd.read_stata(io.BytesIO(data), convert_categoricals=False)
    if ext == "sav":
        import pyreadstat

        with tempfile.NamedTemporaryFile(suffix=".sav", delete=False) as tf:
            tf.write(data)
            path = tf.name
        try:
            df, _ = pyreadstat.read_sav(path)
        finally:
            os.unlink(path)
        return df
    raise RuntimeError(f"unsupported extension: {ext}")


def _sanitize_columns(df):
    seen, cols = {}, []
    for i, raw in enumerate(df.columns):
        name = re.sub(r"[^a-z0-9]+", "_", str(raw).strip().lower()).strip("_")
        if not name or name.startswith("unnamed"):
            name = f"col_{i}"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 1
        cols.append(name)
    df = df.copy()
    df.columns = cols
    return df


def _to_table(df):
    import pyarrow as pa

    df = _sanitize_columns(df)
    # drop fully-empty columns and rows (Excel exports trail junk)
    df = df.dropna(axis=1, how="all").dropna(axis=0, how="all")
    # coerce object columns to string so pyarrow conversion can't trip on
    # mixed-type cells; numeric/datetime/bool columns keep their type.
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].astype("string")
    try:
        return pa.Table.from_pandas(df, preserve_index=False)
    except (pa.ArrowInvalid, pa.ArrowTypeError, pa.ArrowNotImplementedError):
        for c in df.columns:
            df[c] = df[c].astype("string")
        return pa.Table.from_pandas(df, preserve_index=False)


def _stream_parquet_member(data: bytes, member_substr: str, asset: str) -> None:
    """For an already-parquet zip member too large to hold in memory
    (PRIO-GRID, ~36M rows): copy it row-group by row-group into the raw asset."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    _, member_bytes = _zip_member(data, member_substr)
    with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as tf:
        tf.write(member_bytes)
        path = tf.name
    try:
        pf = pq.ParquetFile(path)
        # sanitize the source schema's field names once
        src_names = pf.schema_arrow.names
        rename = {}
        seen = {}
        for i, raw in enumerate(src_names):
            name = re.sub(r"[^a-z0-9]+", "_", str(raw).strip().lower()).strip("_")
            if not name:
                name = f"col_{i}"
            if name in seen:
                seen[name] += 1
                name = f"{name}_{seen[name]}"
            else:
                seen[name] = 1
            rename[raw] = name
        out_schema = pa.schema(
            [pa.field(rename[f.name], f.type) for f in pf.schema_arrow]
        )
        with raw_parquet_writer(asset, out_schema) as w:
            for batch in pf.iter_batches(batch_size=250_000):
                tbl = pa.Table.from_batches([batch]).rename_columns(out_schema.names)
                w.write_table(tbl)
    finally:
        os.unlink(path)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    page_id = node_id[len("prio-"):]
    substr, ext, member = RESOLVE[page_id]

    uuid, fname = _resolve_link(page_id, substr, ext)
    data = _http_get(CDN.format(uuid=uuid, filename=urllib.parse.quote(fname))).content

    if ext == "zip":
        if member.lower().endswith(".parquet"):
            _stream_parquet_member(data, member, asset)
            return
        member_name, member_bytes = _zip_member(data, member)
        member_ext = member_name.rsplit(".", 1)[-1].lower()
        df = _read_dataframe(member_bytes, member_ext, page_id)
    else:
        df = _read_dataframe(data, ext, page_id)

    table = _to_table(df)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"prio-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
