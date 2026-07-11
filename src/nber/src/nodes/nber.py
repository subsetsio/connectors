"""NBER connector — download + transform specs.

Three published tables, all served from the data.nber.org open file server (no
API, just Apache directory indexes):

  - nber-business-cycle-dates : the canonical NBER US recession chronology
    (single small JSON at data.nber.org/cycles/business_cycle_dates.json).
  - nber-macrohistory-series  : the series catalog (title/units/area/source),
    parsed from the parallel docs/<stem>.txt metadata files.
  - nber-macrohistory-values  : long-format observations across all ~3500
    historical series (the .dat rectangular files).

The macrohistory corpus is static; both macrohistory subsets re-enumerate the
chapter indexes and re-fetch every file each run (stateless full re-pull).
"""
import pyarrow as pa
import httpx

from subsets_utils import NodeSpec, raw_parquet_writer, save_raw_parquet
from utils import CHAPTER_NAMES, FREQ_NAMES, MACRO_BASE, _get, _list_chapter_stems

# --------------------------------------------------------------------------- #
# nber-business-cycle-dates
# --------------------------------------------------------------------------- #
CYCLES_URL = "https://data.nber.org/cycles/business_cycle_dates.json"

CYCLES_SCHEMA = pa.schema([
    ("peak", pa.string()),
    ("trough", pa.string()),
])


def fetch_business_cycle_dates(node_id: str) -> None:
    asset = node_id
    data = _get(CYCLES_URL).json()
    rows = [
        {
            "peak": (c.get("peak") or "").strip() or None,
            "trough": (c.get("trough") or "").strip() or None,
        }
        for c in data
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=CYCLES_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# nber-macrohistory-series
# --------------------------------------------------------------------------- #
SERIES_SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("chapter", pa.string()),
    ("chapter_name", pa.string()),
    ("frequency", pa.string()),
    ("title", pa.string()),
    ("units", pa.string()),
    ("area", pa.string()),
    ("source", pa.string()),
])


def _strip_doc_line(raw: str) -> str:
    s = raw.strip()
    if len(s) >= 2 and s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    s = s.strip()
    if s[:1].lower() == "c":  # leading comment marker
        s = s[1:]
    return s.strip()


def _parse_doc(text: str) -> dict:
    """Pull title/units/area/source out of a docs/<stem>.txt metadata file."""
    lines = [_strip_doc_line(r) for r in text.splitlines()]
    title = units = area = source = None
    for i, ln in enumerate(lines):
        up = ln.upper()
        if title is None and len(ln) >= 4 and set(ln) == {"-"}:
            for j in range(i - 1, -1, -1):
                if lines[j].strip():
                    title = lines[j].strip()
                    break
        if units is None and "UNITS:" in up:
            units = ln.split(":", 1)[1].strip() or None
        if area is None and "AREA COVERED:" in up:
            area = ln.split(":", 1)[1].strip() or None
        if source is None and "SOURCE:" in up:
            source = ln.split(":", 1)[1].strip() or None
    return {"title": title, "units": units, "area": area, "source": source}


def fetch_macrohistory_series(node_id: str) -> None:
    asset = node_id
    rows: list[dict] = []
    for chapter in CHAPTER_NAMES:
        for stem in _list_chapter_stems(chapter):
            freq = FREQ_NAMES.get(stem[0])
            if freq is None:
                continue
            meta = {"title": None, "units": None, "area": None, "source": None}
            try:
                text = _get(f"{MACRO_BASE}/{chapter}/docs/{stem}.txt").text
                meta = _parse_doc(text)
            except httpx.HTTPStatusError as e:
                if e.response.status_code != 404:
                    raise  # genuine error — let it propagate
                # no docs file for this series; emit row with empty metadata
            rows.append({
                "series_id": stem,
                "chapter": chapter,
                "chapter_name": CHAPTER_NAMES[chapter],
                "frequency": freq,
                "title": meta["title"],
                "units": meta["units"],
                "area": meta["area"],
                "source": meta["source"],
            })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=SERIES_SCHEMA), asset)


# --------------------------------------------------------------------------- #
# nber-macrohistory-values
# --------------------------------------------------------------------------- #
VALUES_SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("date", pa.string()),
    ("value", pa.float64()),
    ("frequency", pa.string()),
    ("chapter", pa.string()),
])


def _parse_value(tok: str):
    """Parse a macrohistory value token. Returns None for unparseable values and
    the documented missing-data sentinel (MD= 1E-37, i.e. |v| ~ 1e-37)."""
    tok = tok.strip()
    if not tok:
        return None
    try:
        v = float(tok)
    except ValueError:
        return None
    if v != v:  # NaN
        return None
    a = abs(v)
    if a != 0.0 and (a < 1e-30 or a > 1e30):  # missing-data sentinel / garbage
        return None
    return v


def _parse_dat(stem: str, chapter: str, text: str) -> list[dict]:
    freq = stem[0]
    fname = FREQ_NAMES.get(freq)
    if fname is None:  # unknown frequency prefix (one stray 't' file) — skip
        return []
    rows = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) < 2 or not parts[0].isdigit() or len(parts[0]) != 4:
            continue
        year = int(parts[0])
        if freq == "a":
            value = _parse_value(parts[1])
            month = 1
        else:
            if len(parts) < 3 or not parts[1].isdigit():
                continue
            period = int(parts[1])
            value = _parse_value(parts[2])
            if freq == "m":
                if not (1 <= period <= 12):
                    continue
                month = period
            else:  # quarterly
                if not (1 <= period <= 4):
                    continue
                month = (period - 1) * 3 + 1
        if value is None:
            continue
        rows.append({
            "series_id": stem,
            "date": f"{year:04d}-{month:02d}-01",
            "value": value,
            "frequency": fname,
            "chapter": chapter,
        })
    return rows


def fetch_macrohistory_values(node_id: str) -> None:
    asset = node_id
    flush_at = 100_000
    buf: list[dict] = []
    with raw_parquet_writer(asset, VALUES_SCHEMA) as writer:
        for chapter in CHAPTER_NAMES:
            for stem in _list_chapter_stems(chapter):
                text = _get(f"{MACRO_BASE}/{chapter}/{stem}.dat").text
                buf.extend(_parse_dat(stem, chapter, text))
                if len(buf) >= flush_at:
                    writer.write_table(pa.Table.from_pylist(buf, schema=VALUES_SCHEMA))
                    buf = []
        if buf:
            writer.write_table(pa.Table.from_pylist(buf, schema=VALUES_SCHEMA))


# --------------------------------------------------------------------------- #
# specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="nber-business-cycle-dates", fn=fetch_business_cycle_dates, kind="download"),
    NodeSpec(id="nber-macrohistory-series", fn=fetch_macrohistory_series, kind="download"),
    NodeSpec(id="nber-macrohistory-values", fn=fetch_macrohistory_values, kind="download"),
]
