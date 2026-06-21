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
    SqlNodeSpec,
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


def _fetch_xls_urls(urls: list[dict], asset: str) -> None:
    """Read one or more .xls/.xlsx URLs via pandas, optionally tag with a
    `series` column, concatenate, and persist as a single plain CSV."""
    import pandas as pd

    frames = []
    for spec in urls:
        df = pd.read_excel(io.BytesIO(_get_bytes(spec["url"])))
        if spec.get("series"):
            df.insert(0, "series", spec["series"])
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
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
    elif kind == "xls_url":
        _fetch_xls_urls(cfg["urls"], node_id)
    elif kind == "xls_zip":
        _fetch_xls_zip(cfg["url"], cfg["members"][0], node_id)
    else:
        raise ValueError(f"{node_id}: unknown kind {kind!r}")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"cepii-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# --- transforms: one published table per database ----------------------------
# Most are a thin passthrough (DuckDB auto-types the CSV). A couple restore
# zero-padded codes that CSV type inference would strip.

_CUSTOM_SQL = {
    # EQCHANGE ships wide (one column per <country>_<REER|NEER>_TV); reshape to long.
    "cepii-eqchange": '''
        SELECT
            series,
            CAST("Year" AS INTEGER)                                   AS year,
            regexp_replace(country_indicator, '_(REER|NEER)_TV$', '') AS country,
            CAST(value AS DOUBLE)                                     AS index_2010_100
        FROM (
            UNPIVOT "cepii-eqchange"
            ON COLUMNS(* EXCLUDE (series, "Year"))
            INTO NAME country_indicator VALUE value
        )
        WHERE value IS NOT NULL
    ''',
    "cepii-baci": '''
        SELECT
            CAST(t AS INTEGER)                        AS year,
            CAST(i AS INTEGER)                        AS exporter_iso,
            CAST(j AS INTEGER)                        AS importer_iso,
            LPAD(CAST(k AS VARCHAR), 6, '0')          AS product_hs92,
            TRY_CAST(v AS DOUBLE)                     AS value_kusd,
            TRY_CAST(q AS DOUBLE)                     AS quantity_t
        FROM "cepii-baci"
        WHERE t IS NOT NULL
    ''',
    "cepii-macmap-hs6": '''
        SELECT
            LPAD(CAST(reporter AS VARCHAR), 3, '0')   AS reporter_iso,
            LPAD(CAST(partner AS VARCHAR), 3, '0')    AS partner_iso,
            LPAD(CAST(hs2 AS VARCHAR), 2, '0')        AS hs2,
            TRY_CAST(adv AS DOUBLE)                   AS applied_ave,
            TRY_CAST(w_rg AS DOUBLE)                  AS reference_group_weight
        FROM "cepii-macmap-hs6"
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_CUSTOM_SQL.get(s.id, f'SELECT * FROM "{s.id}"'),
    )
    for s in DOWNLOAD_SPECS
]
