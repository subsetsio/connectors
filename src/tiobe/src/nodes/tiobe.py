"""TIOBE Index connector.

Single mechanism: scrape the one static page https://www.tiobe.com/tiobe-index/
(verified in research — all data is server-side, no JS execution needed). The
page is tiny (~130KB) and the only free surface of the source, so every node
does a stateless full re-pull of the whole page and parses its own slice. There
is no incremental filter (the page is a single snapshot + embedded history), so
full re-pull every refresh is correct and cheap.

Five published subsets, each a distinct schema:
  - historical_ratings    : monthly rating time series 2001->now (chart JS)
  - current_rankings      : current-month top 20 (#top20 table)
  - next_50_languages     : ranks 21-50 (#otherPL table)
  - hall_of_fame          : Programming Language of the Year per year (#PLHoF)
  - very_long_term_history: leader positions at ~5y snapshots (#VLTH, unpivoted)
"""

import re
from datetime import date

import lxml.html as LH
import pyarrow as pa

from subsets_utils import NodeSpec, get, transient_retry, save_raw_parquet

URL = "https://www.tiobe.com/tiobe-index/"


@transient_retry()
def _fetch_html() -> str:
    resp = get(URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _doc(html: str):
    return LH.fromstring(html)


def _cell(el) -> str:
    return (el.text_content() or "").strip()


def _pct(s: str):
    """'18.96%' -> 18.96, '+1.30%' -> 1.30, '-6.91%' -> -6.91, '-'/'' -> None."""
    s = (s or "").strip().replace("%", "").replace("+", "")
    if not s or s == "-":
        return None
    return float(s)


def _int(s: str):
    s = (s or "").strip()
    if not s or s == "-":
        return None
    return int(s)


# ----------------------------------------------------------------------------
# historical_ratings — parse the inline Highcharts series array
# ----------------------------------------------------------------------------

# month index in Date.UTC is 0-based; we normalize each point to the first of
# its year-month (research flagged irregular day-of-month values, so we key on
# year-month, not the exact day).
_SERIES_RE = re.compile(r"\{name : '([^']+)',data : \[(.*?)\]\}", re.S)
_POINT_RE = re.compile(r"Date\.UTC\((\d+),\s*(\d+),\s*(\d+)\),\s*([\d.]+)")

_HIST_SCHEMA = pa.schema([
    ("language", pa.string()),
    ("date", pa.date32()),
    ("rating_pct", pa.float64()),
])


def fetch_historical_ratings(node_id: str) -> None:
    html = _fetch_html()
    series = _SERIES_RE.findall(html)
    if not series:
        raise AssertionError("no Highcharts series found — page layout changed")
    # dedup to one row per (language, year-month); last point in a month wins
    rows: dict[tuple, float] = {}
    for language, data in series:
        for y, m0, _d, rating in _POINT_RE.findall(data):
            year, month = int(y), int(m0) + 1
            rows[(language, year, month)] = float(rating)
    out = [
        {"language": lang, "date": date(year, month, 1), "rating_pct": rating}
        for (lang, year, month), rating in rows.items()
    ]
    table = pa.Table.from_pylist(out, schema=_HIST_SCHEMA)
    save_raw_parquet(table, node_id)


# ----------------------------------------------------------------------------
# current_rankings — #top20 table
# ----------------------------------------------------------------------------

_TOP20_SCHEMA = pa.schema([
    ("position", pa.int64()),
    ("prior_year_position", pa.int64()),
    ("language", pa.string()),
    ("rating_pct", pa.float64()),
    ("change_pct", pa.float64()),
])


def fetch_current_rankings(node_id: str) -> None:
    doc = _doc(_fetch_html())
    rows = doc.get_element_by_id("top20").findall(".//tr")
    out = []
    for tr in rows:
        tds = tr.findall("td")
        if len(tds) < 7:
            continue  # header row (th)
        c = [_cell(td) for td in tds]
        # [position, prior_year_position, change_arrow, lang_icon, language, rating, change]
        out.append({
            "position": _int(c[0]),
            "prior_year_position": _int(c[1]),
            "language": c[4],
            "rating_pct": _pct(c[5]),
            "change_pct": _pct(c[6]),
        })
    table = pa.Table.from_pylist(out, schema=_TOP20_SCHEMA)
    save_raw_parquet(table, node_id)


# ----------------------------------------------------------------------------
# next_50_languages — #otherPL table (ranks 21-50)
# ----------------------------------------------------------------------------

_NEXT50_SCHEMA = pa.schema([
    ("position", pa.int64()),
    ("language", pa.string()),
    ("rating_pct", pa.float64()),
])


def fetch_next_50_languages(node_id: str) -> None:
    doc = _doc(_fetch_html())
    rows = doc.get_element_by_id("otherPL").findall(".//tr")
    out = []
    for tr in rows:
        tds = tr.findall("td")
        if len(tds) < 2:
            continue  # header
        c = [_cell(td) for td in tds]
        out.append({
            "position": _int(c[0]),
            "language": c[1],
            "rating_pct": _pct(c[2]) if len(c) > 2 else None,
        })
    table = pa.Table.from_pylist(out, schema=_NEXT50_SCHEMA)
    save_raw_parquet(table, node_id)


# ----------------------------------------------------------------------------
# hall_of_fame — #PLHoF table (Programming Language of the Year per year)
# ----------------------------------------------------------------------------

_HOF_SCHEMA = pa.schema([
    ("year", pa.int64()),
    ("language", pa.string()),
])


def fetch_hall_of_fame(node_id: str) -> None:
    doc = _doc(_fetch_html())
    rows = doc.get_element_by_id("PLHoF").findall(".//tr")
    out = []
    for tr in rows:
        tds = tr.findall("td")
        if len(tds) < 2:
            continue  # header
        year = _int(_cell(tds[0]))
        language = _cell(tds[1])  # medal <img> stripped by text_content()
        if year is None or not language:
            continue
        out.append({"year": year, "language": language})
    table = pa.Table.from_pylist(out, schema=_HOF_SCHEMA)
    save_raw_parquet(table, node_id)


# ----------------------------------------------------------------------------
# very_long_term_history — #VLTH table, unpivoted to long format
# ----------------------------------------------------------------------------

_VLTH_SCHEMA = pa.schema([
    ("language", pa.string()),
    ("snapshot_year", pa.int64()),
    ("position", pa.int64()),
])


def fetch_very_long_term_history(node_id: str) -> None:
    doc = _doc(_fetch_html())
    rows = doc.get_element_by_id("VLTH").findall(".//tr")
    header = [_cell(th) for th in rows[0].findall("th")]
    # header[0] = 'Programming Language'; header[1:] = snapshot years (discovered)
    years = [_int(h) for h in header[1:]]
    out = []
    for tr in rows[1:]:
        tds = tr.findall("td")
        if len(tds) < 2:
            continue
        language = _cell(tds[0])
        for yr, td in zip(years, tds[1:]):
            if yr is None:
                continue
            pos = _int(_cell(td))  # '-' -> None (language absent that snapshot)
            if pos is None:
                continue
            out.append({"language": language, "snapshot_year": yr, "position": pos})
    table = pa.Table.from_pylist(out, schema=_VLTH_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="tiobe-historical-ratings", fn=fetch_historical_ratings, kind="download"),
    NodeSpec(id="tiobe-current-rankings", fn=fetch_current_rankings, kind="download"),
    NodeSpec(id="tiobe-next-50-languages", fn=fetch_next_50_languages, kind="download"),
    NodeSpec(id="tiobe-hall-of-fame", fn=fetch_hall_of_fame, kind="download"),
    NodeSpec(id="tiobe-very-long-term-history", fn=fetch_very_long_term_history, kind="download"),
]
