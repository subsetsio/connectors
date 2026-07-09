"""CEPII connector — one download per CEPII database, one published table each.

Each CEPII database is a distinct bulk file (CSV-in-ZIP, direct CSV, Excel, or
Stata) under cepii.fr. `fetch_one` is a single generic fetcher driven by the
per-database recipe in src/constants.py; it normalizes every source into a
SQL-readable raw asset (gzip CSV / TSV, or a small plain CSV), and the
TRANSFORM_SPECS below publish one Delta table per database from those raws.

Big per-year archives (BACI, TUV, WTFC) are byte-copied member-by-member into
gzip-CSV *batch* files (`<id>-<year>.csv.gz`) with no in-process parse, so memory
stays bounded regardless of corpus size; DuckDB unions the batch at transform
time. Single-file databases write one `<id>.csv.gz`.
"""

from __future__ import annotations

import io
import os
import re
import shutil
import tempfile
import zipfile

from subsets_utils import (
    NodeSpec,
    get_client,
    transient_retry,
    raw_writer,
    save_raw_file,
)
from constants import CONFIG, ENTITY_IDS

CHUNK = 8 * 1024 * 1024
_STREAM_TIMEOUT = 600.0


# --- transport ---------------------------------------------------------------

@transient_retry()
def _stream_to_file(url: str, path: str) -> None:
    """Stream a (possibly multi-GB) URL to a local file with bounded memory."""
    with get_client().stream("GET", url, timeout=_STREAM_TIMEOUT) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_bytes(CHUNK):
                f.write(chunk)


@transient_retry()
def _get_bytes(url: str) -> bytes:
    r = get_client().get(url, timeout=_STREAM_TIMEOUT)
    r.raise_for_status()
    return r.content


# --- writers -----------------------------------------------------------------

def _copy_member_gz(zf: zipfile.ZipFile, member: str, asset: str, ext: str) -> None:
    """Byte-copy one zip member (decompressed) into a gzip raw asset — no parse."""
    with raw_writer(asset, ext, mode="wb", compression="gzip") as out:
        with zf.open(member) as src:
            shutil.copyfileobj(src, out, CHUNK)


@transient_retry()
def _stream_url_to_gz(url: str, asset: str) -> None:
    """Stream a CSV URL straight into a gzip raw asset."""
    with raw_writer(asset, "csv.gz", mode="wb", compression="gzip") as out:
        with get_client().stream("GET", url, timeout=_STREAM_TIMEOUT) as r:
            r.raise_for_status()
            for chunk in r.iter_bytes(CHUNK):
                out.write(chunk)


def _resolve_member(names: list[str], wanted: str) -> str:
    for n in names:
        if os.path.basename(n) == wanted:
            return n
    raise AssertionError(f"member {wanted!r} not found among {names[:8]}")


def _fetch_zip(cfg: dict, asset: str, ext: str) -> None:
    """Download a ZIP to a temp file, then copy selected member(s) to gz raw(s)."""
    tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    tmp.close()
    try:
        _stream_to_file(cfg["url"], tmp.name)
        with zipfile.ZipFile(tmp.name) as zf:
            names = zf.namelist()
            if "member_re" in cfg:
                pat = re.compile(cfg["member_re"])
                selected = sorted(n for n in names if pat.match(os.path.basename(n)))
                if not selected:
                    raise AssertionError(
                        f"{asset}: no members match {cfg['member_re']} in {names[:8]}"
                    )
                for n in selected:
                    stem = os.path.splitext(os.path.basename(n))[0]
                    tag = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-")
                    _copy_member_gz(zf, n, f"{asset}-{tag}", ext)
            else:
                for wanted in cfg["members"]:
                    _copy_member_gz(zf, _resolve_member(names, wanted), asset, ext)
    finally:
        os.unlink(tmp.name)


def _fetch_dta(url: str, asset: str) -> None:
    """Stream a Stata .dta to disk, read it in chunks, emit a gzip CSV."""
    import pandas as pd

    tmp = tempfile.NamedTemporaryFile(suffix=".dta", delete=False)
    tmp.close()
    try:
        _stream_to_file(url, tmp.name)
        reader = pd.read_stata(tmp.name, chunksize=100_000, convert_categoricals=False)
        with raw_writer(asset, "csv.gz", mode="wt", compression="gzip") as out:
            first = True
            for chunk in reader:
                chunk.to_csv(out, index=False, header=first)
                first = False
        if first:
            raise AssertionError(f"{asset}: Stata file produced no rows")
    finally:
        os.unlink(tmp.name)


def _fetch_dta_urls(cfg: dict, asset: str) -> None:
    import pandas as pd

    frames = []
    for spec in cfg["urls"]:
        tmp = tempfile.NamedTemporaryFile(suffix=".dta", delete=False)
        tmp.close()
        try:
            _stream_to_file(spec["url"], tmp.name)
            df = pd.read_stata(tmp.name, convert_categoricals=False)
            df["source_file"] = spec["name"]
            frames.append(df)
        finally:
            os.unlink(tmp.name)
    if not frames:
        raise AssertionError(f"{asset}: no Stata files configured")
    out = pd.concat(frames, ignore_index=True, sort=False)
    buf = io.StringIO()
    out.to_csv(buf, index=False)
    save_raw_file(buf.getvalue(), asset, extension="csv")


def _fetch_eqchange(cfg: dict, asset: str) -> None:
    """EQCHANGE EER index .xls files are wide (Year + one column per country).
    Melt each to long and union REER + NEER with a `series` column."""
    import pandas as pd

    frames = []
    for spec in cfg["urls"]:
        df = pd.read_excel(io.BytesIO(_get_bytes(spec["url"])))
        idc = df.columns[0]  # 'Year'
        long = df.melt(id_vars=[idc], var_name="country_indicator", value_name="value")
        long = long.rename(columns={idc: "year"})
        long["series"] = spec["series"]
        long["country"] = long["country_indicator"].str.replace(
            r"_(REER|NEER)_TV$", "", regex=True
        )
        frames.append(long[["series", "year", "country", "value"]])
    out = pd.concat(frames, ignore_index=True).dropna(subset=["value"])
    buf = io.StringIO()
    out.to_csv(buf, index=False)
    save_raw_file(buf.getvalue(), asset, extension="csv")


def _fetch_rprod(cfg: dict, asset: str) -> None:
    """RPROD.xls holds five Balassa-Samuelson measure sheets (BS1..BS5), each
    country x year x weighting variant. Melt the BS sheets into one long table."""
    import pandas as pd

    xl = pd.ExcelFile(io.BytesIO(_get_bytes(cfg["url"])))
    frames = []
    for sheet in xl.sheet_names:
        if not sheet.upper().startswith("BS"):
            continue
        df = xl.parse(sheet)
        if "Country" not in df.columns or "Year" not in df.columns:
            continue
        long = df.melt(
            id_vars=["Country", "Year"], var_name="indicator", value_name="value"
        )
        long["measure"] = sheet
        frames.append(long[["measure", "Country", "Year", "indicator", "value"]])
    if not frames:
        raise AssertionError(f"{asset}: no BS measure sheets found in RPROD.xls")
    out = pd.concat(frames, ignore_index=True).dropna(subset=["value"])
    buf = io.StringIO()
    out.to_csv(buf, index=False)
    save_raw_file(buf.getvalue(), asset, extension="csv")


def _fetch_xls_zip(url: str, member: str, asset: str) -> None:
    import pandas as pd

    zf = zipfile.ZipFile(io.BytesIO(_get_bytes(url)))
    real = _resolve_member(zf.namelist(), member)
    df = pd.read_excel(io.BytesIO(zf.read(real)))
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    save_raw_file(buf.getvalue(), asset, extension="csv")


def _fetch_xls_urls(cfg: dict, asset: str) -> None:
    import pandas as pd

    frames = []
    for spec in cfg["urls"]:
        xl = pd.ExcelFile(io.BytesIO(_get_bytes(spec["url"])))
        sheets = spec.get("sheets") or xl.sheet_names
        for sheet in sheets:
            df = xl.parse(sheet)
            if df.empty:
                continue
            df["source_file"] = spec["name"]
            df["source_sheet"] = sheet
            frames.append(df)
    if not frames:
        raise AssertionError(f"{asset}: no non-empty Excel sheets found")
    out = pd.concat(frames, ignore_index=True, sort=False)
    buf = io.StringIO()
    out.to_csv(buf, index=False)
    save_raw_file(buf.getvalue(), asset, extension="csv")


def _fetch_text_urls(cfg: dict, asset: str, ext: str) -> None:
    with raw_writer(asset, ext, mode="wb", compression="gzip") as out:
        first = True
        for spec in cfg["urls"]:
            body = _get_bytes(spec["url"])
            lines = body.splitlines(keepends=True)
            if not lines:
                continue
            if first:
                out.write(b"source_file" + cfg["delimiter"].encode("ascii") + lines[0])
                first = False
            for line in lines[1:]:
                out.write(spec["name"].encode("utf-8") + cfg["delimiter"].encode("ascii") + line)
    if first:
        raise AssertionError(f"{asset}: no text rows fetched")


# --- the single generic fetch fn --------------------------------------------

def fetch_one(node_id: str) -> None:
    entity = node_id[len("cepii-"):]
    cfg = CONFIG[entity]
    kind = cfg["kind"]
    if kind == "csv_zip":
        _fetch_zip(cfg, node_id, "csv.gz")
    elif kind == "tsv_zip":
        _fetch_zip(cfg, node_id, "tsv.gz")
    elif kind == "csv_url":
        _stream_url_to_gz(cfg["url"], node_id)
    elif kind == "dta_url":
        _fetch_dta(cfg["url"], node_id)
    elif kind == "dta_urls":
        _fetch_dta_urls(cfg, node_id)
    elif kind == "eqchange":
        _fetch_eqchange(cfg, node_id)
    elif kind == "rprod":
        _fetch_rprod(cfg, node_id)
    elif kind == "xls_zip":
        _fetch_xls_zip(cfg["url"], cfg["members"][0], node_id)
    elif kind == "xls_urls":
        _fetch_xls_urls(cfg, node_id)
    elif kind == "tsv_urls":
        _fetch_text_urls(cfg, node_id, "tsv.gz")
    elif kind == "csv_semicolon_url":
        _stream_url_to_gz(cfg["url"], node_id)
    else:
        raise ValueError(f"{node_id}: unknown kind {kind!r}")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"cepii-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
