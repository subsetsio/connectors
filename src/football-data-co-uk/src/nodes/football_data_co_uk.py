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
    SqlNodeSpec,
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

_MAIN = "football-data-co-uk-matches-main"
_EXTRA = "football-data-co-uk-matches-extra"

# Date columns are dd/mm/yyyy in modern files and dd/mm/yy in older ones; try
# both. TRY_CAST/NULLIF turn empty cells and malformed values into nulls
# instead of failing the whole query.
# Try the 2-digit-year format first: '%Y' would wrongly parse a 2-digit
# "93" as year 0093, whereas '%y' fails cleanly on a 4-digit year and falls
# through to '%Y'. DuckDB maps %y 70-99 -> 1970-1999, 00-69 -> 2000-2069,
# which is correct for this corpus (earliest season 1993).
_DATE = (
    'COALESCE(TRY_STRPTIME("Date", \'%d/%m/%y\'), '
    'TRY_STRPTIME("Date", \'%d/%m/%Y\'))::DATE'
)

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_MAIN}-transform",
        deps=[_MAIN],
        sql=f'''
            SELECT
                "Season"                                AS season,
                "Div"                                   AS division,
                {_DATE}                                 AS date,
                NULLIF("Time", '')                      AS kickoff_time,
                "HomeTeam"                              AS home_team,
                "AwayTeam"                              AS away_team,
                TRY_CAST("FTHG" AS INTEGER)             AS ft_home_goals,
                TRY_CAST("FTAG" AS INTEGER)             AS ft_away_goals,
                "FTR"                                   AS ft_result,
                TRY_CAST("HTHG" AS INTEGER)             AS ht_home_goals,
                TRY_CAST("HTAG" AS INTEGER)             AS ht_away_goals,
                "HTR"                                   AS ht_result,
                "Referee"                               AS referee,
                TRY_CAST("HS"  AS INTEGER)              AS home_shots,
                TRY_CAST("AS"  AS INTEGER)              AS away_shots,
                TRY_CAST("HST" AS INTEGER)              AS home_shots_target,
                TRY_CAST("AST" AS INTEGER)              AS away_shots_target,
                TRY_CAST("HF"  AS INTEGER)              AS home_fouls,
                TRY_CAST("AF"  AS INTEGER)              AS away_fouls,
                TRY_CAST("HC"  AS INTEGER)              AS home_corners,
                TRY_CAST("AC"  AS INTEGER)              AS away_corners,
                TRY_CAST("HY"  AS INTEGER)              AS home_yellows,
                TRY_CAST("AY"  AS INTEGER)              AS away_yellows,
                TRY_CAST("HR"  AS INTEGER)              AS home_reds,
                TRY_CAST("AR"  AS INTEGER)              AS away_reds,
                TRY_CAST("B365H" AS DOUBLE)             AS b365_home,
                TRY_CAST("B365D" AS DOUBLE)             AS b365_draw,
                TRY_CAST("B365A" AS DOUBLE)             AS b365_away,
                TRY_CAST("MaxH" AS DOUBLE)              AS max_home,
                TRY_CAST("MaxD" AS DOUBLE)              AS max_draw,
                TRY_CAST("MaxA" AS DOUBLE)              AS max_away,
                TRY_CAST("AvgH" AS DOUBLE)              AS avg_home,
                TRY_CAST("AvgD" AS DOUBLE)              AS avg_draw,
                TRY_CAST("AvgA" AS DOUBLE)              AS avg_away,
                TRY_CAST("Avg>2.5" AS DOUBLE)           AS avg_over_2_5,
                TRY_CAST("Avg<2.5" AS DOUBLE)           AS avg_under_2_5,
                TRY_CAST("AvgCH" AS DOUBLE)             AS avg_close_home,
                TRY_CAST("AvgCD" AS DOUBLE)             AS avg_close_draw,
                TRY_CAST("AvgCA" AS DOUBLE)             AS avg_close_away,
                TRY_CAST("AHh" AS DOUBLE)               AS asian_handicap_line,
                TRY_CAST("AvgAHH" AS DOUBLE)            AS avg_ah_home,
                TRY_CAST("AvgAHA" AS DOUBLE)            AS avg_ah_away
            FROM "{_MAIN}"
            WHERE "HomeTeam" IS NOT NULL AND "AwayTeam" IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{_EXTRA}-transform",
        deps=[_EXTRA],
        sql=f'''
            SELECT
                "Country"                               AS country,
                TRIM("League")                          AS league,
                "Season"                                AS season,
                {_DATE}                                 AS date,
                NULLIF("Time", '')                      AS kickoff_time,
                "Home"                                  AS home_team,
                "Away"                                  AS away_team,
                TRY_CAST("HG" AS INTEGER)               AS home_goals,
                TRY_CAST("AG" AS INTEGER)               AS away_goals,
                "Res"                                   AS result,
                TRY_CAST("PSCH" AS DOUBLE)              AS pinnacle_close_home,
                TRY_CAST("PSCD" AS DOUBLE)              AS pinnacle_close_draw,
                TRY_CAST("PSCA" AS DOUBLE)              AS pinnacle_close_away,
                TRY_CAST("MaxCH" AS DOUBLE)             AS max_close_home,
                TRY_CAST("MaxCD" AS DOUBLE)             AS max_close_draw,
                TRY_CAST("MaxCA" AS DOUBLE)             AS max_close_away,
                TRY_CAST("AvgCH" AS DOUBLE)             AS avg_close_home,
                TRY_CAST("AvgCD" AS DOUBLE)             AS avg_close_draw,
                TRY_CAST("AvgCA" AS DOUBLE)             AS avg_close_away,
                TRY_CAST("BFECH" AS DOUBLE)             AS betfair_close_home,
                TRY_CAST("BFECD" AS DOUBLE)             AS betfair_close_draw,
                TRY_CAST("BFECA" AS DOUBLE)             AS betfair_close_away,
                TRY_CAST("B365CH" AS DOUBLE)            AS b365_close_home,
                TRY_CAST("B365CD" AS DOUBLE)            AS b365_close_draw,
                TRY_CAST("B365CA" AS DOUBLE)            AS b365_close_away
            FROM "{_EXTRA}"
            WHERE "Home" IS NOT NULL AND "Away" IS NOT NULL
        ''',
    ),
]
