"""CEPII connector — one download per CEPII database, one published table each.

Each CEPII database is a distinct bulk file (CSV-in-ZIP, direct CSV, Excel, or
Stata) under cepii.fr. `fetch_one` is a single generic fetcher driven by the
per-database recipe in src/constants.py; it normalizes every source into a
SQL-readable raw asset (gzip CSV / TSV, or a small plain CSV), and the
TRANSFORM_SPECS below publish one Delta table per database from those raws.

Big per-year archives (BACI, TUV, WTFC) stream member-by-member into parquet
fragments, so memory stays bounded regardless of corpus size and downstream
profiling/transforms read columnar raw. Single-file databases write one raw
object.
"""

from __future__ import annotations

import io
import csv
import os
import re
import struct
import tempfile
import zipfile

from subsets_utils import (
    NodeSpec,
    get_client,
    transient_retry,
    raw_writer,
    raw_parquet_writer,
    save_raw_file,
)
from constants import CONFIG, ENTITY_IDS

CHUNK = 8 * 1024 * 1024
_STREAM_TIMEOUT = 600.0
_WK1_SIGNATURES = (b"\x00\x00\x02\x00\x04\x04", b"\x00\x00\x02\x00\x06\x04")


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

def _copy_member_parquet(
    zf: zipfile.ZipFile,
    member: str,
    asset: str,
    *,
    delimiter: str = ",",
    fragment: str | None = None,
) -> None:
    """Stream one ZIP member into a parquet raw fragment."""
    import pyarrow.csv as pacsv

    parse_options = pacsv.ParseOptions(delimiter=delimiter)
    read_options = pacsv.ReadOptions(encoding="utf-8-sig")
    convert_options = pacsv.ConvertOptions(strings_can_be_null=True)

    with zf.open(member) as src:
        reader = pacsv.open_csv(
            src,
            read_options=read_options,
            parse_options=parse_options,
            convert_options=convert_options,
        )
        with raw_parquet_writer(asset, reader.schema, fragment=fragment) as writer:
            for batch in reader:
                writer.write_batch(batch)


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


def _fetch_zip(cfg: dict, asset: str, *, delimiter: str = ",") -> None:
    """Download a ZIP to a temp file, then stream selected member(s) to parquet."""
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
                    _copy_member_parquet(zf, n, asset, delimiter=delimiter, fragment=tag)
            else:
                for wanted in cfg["members"]:
                    member = _resolve_member(names, wanted)
                    _copy_member_parquet(zf, member, asset, delimiter=delimiter)
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
        body = _get_bytes(spec["url"])
        if body.startswith(_WK1_SIGNATURES):
            df = _parse_wk1(body)
            if not df.empty:
                df["source_file"] = spec["name"]
                df["source_sheet"] = "wk1"
                frames.append(df)
            continue

        xl = pd.ExcelFile(io.BytesIO(body))
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


def _parse_wk1(body: bytes):
    """Read simple Lotus 1-2-3 WK1 worksheets used by CEPII legacy files."""
    import pandas as pd

    cells: dict[tuple[int, int], object] = {}
    pos = 0
    while pos + 4 <= len(body):
        opcode, length = struct.unpack_from("<HH", body, pos)
        pos += 4
        payload = body[pos : pos + length]
        pos += length

        if opcode == 0x01:  # EOF
            break
        if opcode == 0x0F and length >= 6:  # LABEL
            col = int.from_bytes(payload[1:3], "little")
            row = int.from_bytes(payload[3:5], "little")
            text = payload[5:].rstrip(b"\x00").decode("latin-1", errors="replace")
            if text[:1] in {"'", '"', "^", "\\"}:
                text = text[1:]
            cells[(row, col)] = text
        elif opcode == 0x0E and length >= 13:  # NUMBER
            col = int.from_bytes(payload[1:3], "little")
            row = int.from_bytes(payload[3:5], "little")
            cells[(row, col)] = struct.unpack("<d", payload[5:13])[0]
        elif opcode == 0x0D and length >= 7:  # INTEGER
            col = int.from_bytes(payload[1:3], "little")
            row = int.from_bytes(payload[3:5], "little")
            cells[(row, col)] = int.from_bytes(payload[5:7], "little", signed=True)

    if not cells:
        return pd.DataFrame()

    max_row = max(row for row, _ in cells)
    max_col = max(col for _, col in cells)
    grid = [
        [cells.get((row, col)) for col in range(max_col + 1)]
        for row in range(max_row + 1)
    ]
    header = grid[0]
    columns = [
        str(value).strip() if value not in (None, "") else f"col_{idx}"
        for idx, value in enumerate(header)
    ]
    return pd.DataFrame(grid[1:], columns=columns).dropna(how="all")


def _fetch_text_urls(cfg: dict, asset: str) -> None:
    with raw_writer(asset, "csv.gz", mode="wt", compression="gzip") as out:
        writer = csv.writer(out)
        first = True
        for spec in cfg["urls"]:
            body = _get_bytes(spec["url"])
            text = body.decode("utf-8-sig", errors="replace").splitlines()
            rows = list(csv.reader(text, delimiter=cfg["delimiter"]))
            if not rows:
                continue
            if first:
                writer.writerow(["source_file", *rows[0]])
                first = False
            for row in rows[1:]:
                writer.writerow([spec["name"], *row])
    if first:
        raise AssertionError(f"{asset}: no text rows fetched")


# --- the single generic fetch fn --------------------------------------------

def fetch_one(node_id: str) -> None:
    entity = node_id[len("cepii-"):]
    cfg = CONFIG[entity]
    kind = cfg["kind"]
    if kind == "csv_zip":
        _fetch_zip(cfg, node_id)
    elif kind == "tsv_zip":
        _fetch_zip(cfg, node_id, delimiter="\t")
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
        _fetch_text_urls(cfg, node_id)
    elif kind == "csv_semicolon_url":
        _stream_url_to_gz(cfg["url"], node_id)
    else:
        raise ValueError(f"{node_id}: unknown kind {kind!r}")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"cepii-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
