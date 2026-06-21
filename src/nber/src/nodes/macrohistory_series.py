"""NBER Macrohistory Database — the series catalog (title/units/area/source).

For each .dat series under data.nber.org/databases/macrohistory/rectdata/, the
descriptive title/units/source live in the parallel docs/<stem>.txt file. This
subset enumerates the chapter indexes and parses those metadata files.

Fetch shape: stateless full re-pull, matching the values subset.
"""
import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import CHAPTER_NAMES, FREQ_NAMES, MACRO_BASE, _get, _list_chapter_stems

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


DOWNLOAD_SPECS = [
    NodeSpec(id="nber-macrohistory-series", fn=fetch_macrohistory_series, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nber-macrohistory-series-transform",
        deps=["nber-macrohistory-series"],
        sql='''
            SELECT
                series_id,
                chapter,
                chapter_name,
                frequency,
                title,
                units,
                area,
                source
            FROM "nber-macrohistory-series"
        ''',
    ),
]
