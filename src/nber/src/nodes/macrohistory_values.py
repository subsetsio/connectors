"""NBER Macrohistory Database — long-format observations across all series.

~3500 historical economic time series organized in 16 chapter directories under
data.nber.org/databases/macrohistory/rectdata/<chapter>/. Each series is a plain
-text rectangular .dat file (annual `YYYY value`, monthly `YYYY MM value`,
quarterly `YYYY Q value`).

Fetch shape: stateless full re-pull. The corpus is static and small, so we
re-enumerate the chapter indexes and re-fetch every file each run and overwrite.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer
from utils import CHAPTER_NAMES, FREQ_NAMES, MACRO_BASE, _get, _list_chapter_stems

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


DOWNLOAD_SPECS = [
    NodeSpec(id="nber-macrohistory-values", fn=fetch_macrohistory_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nber-macrohistory-values-transform",
        deps=["nber-macrohistory-values"],
        sql='''
            SELECT
                series_id,
                CAST(date AS DATE) AS date,
                CAST(value AS DOUBLE) AS value,
                frequency,
                chapter
            FROM "nber-macrohistory-values"
            WHERE value IS NOT NULL
        ''',
    ),
]
