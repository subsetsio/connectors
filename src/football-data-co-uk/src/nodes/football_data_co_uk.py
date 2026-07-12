"""football-data.co.uk connector.

Two published subsets, each assembled from many per-file CSV bulk downloads
that are discovered at runtime from the source's per-country index pages
(the site has no machine-readable catalog; data.php links country pages, each
country page links the actual CSVs):

- matches_main: the 11 "main" European leagues. One CSV per (season, division)
  at mmz4281/{season}/{div}.csv (season is a 4-digit code, e.g. 2425 = 2024/25).
  Wide schema: results + match stats + many bookmaker odds columns; older
  seasons carry fewer columns. ~690 files, one season's worth of one division
  each. Season is NOT a column in these files, so we inject it from the URL.
- matches_extra: the 16 "extra" leagues. One CSV per country at new/{cc}.csv,
  each stacking every season for that country. Normalized schema that already
  carries Country/League/Season columns. 16 files.

Fetch shape: stateless full re-pull each run. The whole corpus is a few hundred
CSVs / a few hundred MB, the current-season main files are overwritten in place
upstream (updated twice weekly), and there is no incremental/`since` filter, so
re-fetching everything every run is cheap and picks up revisions for free.

Raw is written as parquet with an explicit all-string schema (faithful to the
CSV text — values stay exactly as published); the SQL transform is the typing
and correctness gate (cast, parse dates, drop blanks).
"""

import csv
import io
import re

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://www.football-data.co.uk"

# Stable site structure (which index pages to read) — the actual seasons,
# divisions and country codes are discovered from these pages at runtime.
MAIN_PAGES = [
    "englandm", "scotlandm", "germanym", "italym", "spainm", "francem",
    "netherlandsm", "belgiumm", "portugalm", "turkeym", "greecem",
]
EXTRA_PAGES = [
    "Argentina", "Austria", "Brazil", "China", "Denmark", "Finland",
    "Ireland", "Japan", "Mexico", "Norway", "Poland", "Romania", "Russia",
    "Sweden", "Switzerland", "USA",
]

# Curated column projection for the wide main-league files (a stable superset;
# we keep core results, match stats, the Bet365 / market-average / market-max
# odds, over/under 2.5 and the Asian-handicap line). "Season" is injected from
# the URL. Columns absent from a given (older) file come through as null.
MAIN_COLS = [
    "Season", "Div", "Date", "Time", "HomeTeam", "AwayTeam",
    "FTHG", "FTAG", "FTR", "HTHG", "HTAG", "HTR",
    "Referee", "HS", "AS", "HST", "AST", "HF", "AF", "HC", "AC",
    "HY", "AY", "HR", "AR",
    "B365H", "B365D", "B365A",
    "MaxH", "MaxD", "MaxA", "AvgH", "AvgD", "AvgA",
    "Avg>2.5", "Avg<2.5",
    "AvgCH", "AvgCD", "AvgCA",
    "AHh", "AvgAHH", "AvgAHA",
]

# Normalized schema of the extra-league files (consistent across countries).
EXTRA_COLS = [
    "Country", "League", "Season", "Date", "Time", "Home", "Away",
    "HG", "AG", "Res",
    "PSCH", "PSCD", "PSCA",
    "MaxCH", "MaxCD", "MaxCA",
    "AvgCH", "AvgCD", "AvgCA",
    "BFECH", "BFECD", "BFECA",
    "B365CH", "B365CD", "B365CA",
]

MAIN_SCHEMA = pa.schema([(c, pa.string()) for c in MAIN_COLS])
EXTRA_SCHEMA = pa.schema([(c, pa.string()) for c in EXTRA_COLS])

MMZ_RE = re.compile(r"mmz4281/(\d{4})/([A-Za-z0-9]+)\.csv")
NEW_RE = re.compile(r"new/([A-Za-z0-9]+)\.csv")


@transient_retry()
def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    # CSVs (and the html headers) are UTF-8 with a leading BOM; utf-8-sig
    # strips it so the first column header maps cleanly.
    return resp.content.decode("utf-8-sig", errors="replace")


def _season_label(code: str) -> str:
    """'9394' -> '1993/1994', '2425' -> '2024/2025'."""
    y1, y2 = int(code[:2]), int(code[2:])
    start = 1900 + y1 if y1 >= 90 else 2000 + y1
    end = 1900 + y2 if y2 >= 90 else 2000 + y2
    return f"{start}/{end}"


def _parse_csv(text: str, cols: list, extra: dict | None = None) -> list:
    rows = []
    for raw in csv.DictReader(io.StringIO(text)):
        rec = {}
        for c in cols:
            v = raw.get(c)
            rec[c] = None if v in (None, "") else v
        if extra:
            rec.update(extra)
        rows.append(rec)
    return rows


def _discover_main() -> list:
    """Return sorted unique (season, division) pairs across all main pages."""
    pairs = set()
    for page in MAIN_PAGES:
        html = _get_text(f"{BASE}/{page}.php")
        pairs.update(MMZ_RE.findall(html))
    # Safety ceiling: the source has ~690 such files. A big shortfall means an
    # index page changed format and discovery silently broke — raise, never
    # publish a truncated corpus.
    if len(pairs) < 400:
        raise AssertionError(
            f"main discovery found only {len(pairs)} (season, division) files; "
            "index-page format may have changed"
        )
    return sorted(pairs)


def _discover_extra() -> list:
    codes = set()
    for page in EXTRA_PAGES:
        html = _get_text(f"{BASE}/{page}.php")
        codes.update(NEW_RE.findall(html))
    if len(codes) < 10:
        raise AssertionError(
            f"extra discovery found only {len(codes)} country files; "
            "index-page format may have changed"
        )
    return sorted(codes)


def fetch_main(node_id: str) -> None:
    asset = node_id
    rows = []
    for season, div in _discover_main():
        text = _get_text(f"{BASE}/mmz4281/{season}/{div}.csv")
        parsed = _parse_csv(text, MAIN_COLS, extra={"Season": _season_label(season)})
        # Drop trailing blank lines (no teams).
        rows.extend(r for r in parsed if r.get("HomeTeam") and r.get("AwayTeam"))
    table = pa.Table.from_pylist(rows, schema=MAIN_SCHEMA)
    save_raw_parquet(table, asset)


def fetch_extra(node_id: str) -> None:
    asset = node_id
    rows = []
    for cc in _discover_extra():
        text = _get_text(f"{BASE}/new/{cc}.csv")
        parsed = _parse_csv(text, EXTRA_COLS)
        rows.extend(r for r in parsed if r.get("Home") and r.get("Away"))
    table = pa.Table.from_pylist(rows, schema=EXTRA_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="football-data-co-uk-matches-main", fn=fetch_main, kind="download"),
    NodeSpec(id="football-data-co-uk-matches-extra", fn=fetch_extra, kind="download"),
]
