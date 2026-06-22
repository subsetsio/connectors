"""Box Office Mojo connector.

Box Office Mojo (IMDb/Amazon) exposes no free machine-readable API; its public
surface is server-rendered static HTML report tables with stable URL patterns.
Each report page carries exactly one HTML <table>, parsed here with
pandas.read_html. Raw is saved as NDJSON of *string* cell values exactly as
scraped (gross like "$636,225,983", dashes "-" for missing); all typing,
currency/percent parsing and date construction happens in the DuckDB transform
SQL, which is the correctness gate.

Shape: stateless full re-pull (shape 1). Historical pages are immutable; the
current year / recent weekends change, so every refresh re-fetches the full
corpus and overwrites. No incremental filter exists on this source. The
year/weekend/day dimension is a column value, not a separate subset, so each
report *family* is one download asset accumulating every period.

The weekend release-level family crawls every weekend detail page (~50 weekends
x ~45 tracked years ~= 2300 pages); this is the long-pole node by design.
"""

import io
import re

import pandas as pd

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://www.boxofficemojo.com"


# --------------------------------------------------------------------------- #
# HTTP + parsing helpers
# --------------------------------------------------------------------------- #
@transient_retry()  # 6 attempts, exp backoff 4..120s; retries 429/5xx/transient
def _get_html(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _read_table(html: str):
    """Return the first HTML table as a DataFrame, or None if the page has none
    (e.g. a year before that report type was tracked)."""
    try:
        # Default flavor: pandas tries lxml first and falls back to
        # bs4+html5lib on pages lxml-html chokes on (some weekend detail pages
        # have malformed markup). All three parsers are pinned as deps.
        tables = pd.read_html(io.StringIO(html))
    except ValueError:
        return None
    return tables[0] if tables else None


def _str_rows(df: pd.DataFrame, colmap: dict, extra: dict | None = None) -> list[dict]:
    """Project/rename columns per colmap and stringify every cell (NaN -> None),
    appending the constant `extra` identity fields to each row."""
    rows = []
    cols = [c for c in colmap if c in df.columns]
    for rec in df[cols].to_dict("records"):
        row = {} if extra is None else dict(extra)
        for src in cols:
            val = rec[src]
            row[colmap[src]] = None if pd.isna(val) else str(val)
        rows.append(row)
    return rows


def _discover_years() -> list[str]:
    """The /year/ index links to every available domestic year (e.g. 1977-2026).
    Years are data, discovered from the source, never a hardcoded range."""
    html = _get_html(f"{BASE}/year/")
    years = sorted(set(re.findall(r"/year/(\d{4})/", html)))
    if len(years) < 20:
        raise AssertionError(f"year index yielded only {len(years)} years; page format changed")
    return years


# --------------------------------------------------------------------------- #
# Column maps (raw HTML header -> clean snake_case key)
# --------------------------------------------------------------------------- #
YEARLY_SUMMARY_COLS = {
    "Year": "year", "Total Gross": "total_gross", "%± LY": "change_pct",
    "Releases": "releases", "Average": "average", "#1 Release": "num1_release",
}
DOMESTIC_YEARLY_COLS = {
    "Rank": "rank", "Release": "release", "Genre": "genre", "Budget": "budget",
    "Running Time": "running_time", "Gross": "gross", "Theaters": "theaters",
    "Total Gross": "total_gross", "Release Date": "release_date",
    "Distributor": "distributor", "Estimated": "estimated",
}
WORLDWIDE_YEARLY_COLS = {
    "Rank": "rank", "Release Group": "release_group", "Worldwide": "worldwide",
    "Domestic": "domestic", "%": "domestic_pct", "Foreign": "foreign",
    "%.1": "foreign_pct",
}
WEEKEND_SUMMARY_COLS = {
    "Dates": "dates", "Top 10 Gross": "top10_gross", "%± LW": "top10_change_pct",
    "Overall Gross": "overall_gross", "%± LW.1": "overall_change_pct",
    "Releases": "releases", "#1 Release": "num1_release", "Week": "week",
    "Long Weekend": "long_weekend",
}
WEEKEND_DETAIL_COLS = {
    "Rank": "rank", "LW": "last_week_rank", "Release": "release", "Gross": "gross",
    "%± LW": "weekend_change_pct", "Theaters": "theaters", "Change": "theater_change",
    "Average": "average", "Total Gross": "total_gross", "Weeks": "weeks",
    "Distributor": "distributor", "New This Week": "new_this_week",
    "Estimated": "estimated",
}
DAILY_COLS = {
    "Date": "date_raw", "Day": "day_of_week", "Day #": "day_num",
    "Top 10 Gross": "top10_gross", "%± YD": "change_yd_pct", "%± LW": "change_lw_pct",
    "Releases": "releases", "#1 Release": "num1_release", "Gross": "gross",
}
TOP_LIFETIME_COLS = {
    "Rank": "rank", "Title": "title", "Lifetime Gross": "lifetime_gross", "Year": "year",
}


# --------------------------------------------------------------------------- #
# Fetch functions — one per entity (the spec id IS the asset name)
# --------------------------------------------------------------------------- #
def fetch_yearly_summary(node_id: str) -> None:
    html = _get_html(f"{BASE}/year/")
    df = _read_table(html)
    if df is None:
        raise AssertionError("domestic /year/ index returned no table")
    save_raw_ndjson(_str_rows(df, YEARLY_SUMMARY_COLS), node_id)


def fetch_domestic_yearly(node_id: str) -> None:
    rows = []
    for year in _discover_years():
        df = _read_table(_get_html(f"{BASE}/year/{year}/"))
        if df is not None:
            rows.extend(_str_rows(df, DOMESTIC_YEARLY_COLS, {"year": year}))
    save_raw_ndjson(rows, node_id)


def fetch_worldwide_yearly(node_id: str) -> None:
    rows = []
    for year in _discover_years():
        df = _read_table(_get_html(f"{BASE}/year/world/{year}/"))
        if df is not None:
            rows.extend(_str_rows(df, WORLDWIDE_YEARLY_COLS, {"year": year}))
    save_raw_ndjson(rows, node_id)


def fetch_weekend_summary(node_id: str) -> None:
    rows = []
    for year in _discover_years():
        df = _read_table(_get_html(f"{BASE}/weekend/?yr={year}"))
        if df is not None:
            rows.extend(_str_rows(df, WEEKEND_SUMMARY_COLS, {"year": year}))
    save_raw_ndjson(rows, node_id)


def fetch_domestic_weekend(node_id: str) -> None:
    rows = []
    for year in _discover_years():
        index_html = _get_html(f"{BASE}/weekend/?yr={year}")
        weekend_ids = sorted(set(re.findall(r"/weekend/(\d{4}W\d{2})/", index_html)))
        for wid in weekend_ids:
            df = _read_table(_get_html(f"{BASE}/weekend/{wid}/"))
            if df is not None:
                week = wid[5:].lstrip("0") or "0"
                rows.extend(_str_rows(df, WEEKEND_DETAIL_COLS,
                                      {"weekend_id": wid, "year": year, "week": week}))
    save_raw_ndjson(rows, node_id)


def fetch_domestic_daily(node_id: str) -> None:
    rows = []
    for year in _discover_years():
        df = _read_table(_get_html(f"{BASE}/daily/{year}/"))
        if df is not None:
            rows.extend(_str_rows(df, DAILY_COLS, {"year": year}))
    save_raw_ndjson(rows, node_id)


MAX_CHART_PAGES = 500  # safety ceiling: raises if the chart grows past expectation


def fetch_top_lifetime_grosses(node_id: str) -> None:
    rows = []
    offset = 0
    for _ in range(MAX_CHART_PAGES):
        url = f"{BASE}/chart/top_lifetime_gross/?offset={offset}" if offset \
            else f"{BASE}/chart/top_lifetime_gross/"
        df = _read_table(_get_html(url))
        if df is None or len(df) == 0:
            break
        rows.extend(_str_rows(df, TOP_LIFETIME_COLS))
        if len(df) < 200:  # last (partial) page
            break
        offset += 200
    else:
        raise AssertionError(f"top_lifetime_gross exceeded {MAX_CHART_PAGES} pages; cap hit")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="box-office-mojo-yearly-summary",      fn=fetch_yearly_summary,      kind="download"),
    NodeSpec(id="box-office-mojo-domestic-yearly",     fn=fetch_domestic_yearly,     kind="download"),
    NodeSpec(id="box-office-mojo-worldwide-yearly",    fn=fetch_worldwide_yearly,    kind="download"),
    NodeSpec(id="box-office-mojo-weekend-summary",     fn=fetch_weekend_summary,     kind="download"),
    NodeSpec(id="box-office-mojo-domestic-weekend",    fn=fetch_domestic_weekend,    kind="download"),
    NodeSpec(id="box-office-mojo-domestic-daily",      fn=fetch_domestic_daily,      kind="download"),
    NodeSpec(id="box-office-mojo-top-lifetime-grosses", fn=fetch_top_lifetime_grosses, kind="download"),
]


# --------------------------------------------------------------------------- #
# Transform SQL helpers (DuckDB) — parse the scraped strings into typed columns
# --------------------------------------------------------------------------- #
def _money(col: str) -> str:      # "$636,225,983" / "-" -> BIGINT
    return f"TRY_CAST(regexp_replace({col}, '[^0-9]', '', 'g') AS BIGINT)"

def _int(col: str) -> str:        # "4337" / "-" -> INTEGER
    return f"TRY_CAST(regexp_replace({col}, '[^0-9]', '', 'g') AS INTEGER)"

def _sint(col: str) -> str:       # "-385" -> INTEGER (keeps sign)
    return f"TRY_CAST(regexp_replace({col}, '[^0-9-]', '', 'g') AS INTEGER)"

def _pct(col: str) -> str:        # "+19.4%" / "-34.2%" / "-" -> DOUBLE
    return f"TRY_CAST(regexp_replace({col}, '[^0-9.-]', '', 'g') AS DOUBLE)"

def _bool(col: str) -> str:       # "True"/"False"/null -> BOOLEAN
    return f"({col} = 'True')"


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="box-office-mojo-yearly-summary-transform",
        deps=["box-office-mojo-yearly-summary"],
        sql=f'''
            SELECT
                CAST(year AS INTEGER)        AS year,
                {_money('total_gross')}      AS total_gross,
                {_pct('change_pct')}         AS change_vs_prior_year_pct,
                {_int('releases')}           AS releases,
                {_money('average')}          AS average_gross,
                num1_release                 AS num1_release
            FROM "box-office-mojo-yearly-summary"
            WHERE TRY_CAST(year AS INTEGER) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="box-office-mojo-domestic-yearly-transform",
        deps=["box-office-mojo-domestic-yearly"],
        sql=f'''
            SELECT
                CAST(year AS INTEGER)   AS year,
                {_int('rank')}          AS rank,
                release                 AS release,
                {_money('gross')}       AS gross,
                {_int('theaters')}      AS theaters,
                {_money('total_gross')} AS total_gross,
                NULLIF(release_date, '-') AS release_date,
                NULLIF(distributor, '-')  AS distributor,
                NULLIF(genre, '-')        AS genre,
                {_bool('estimated')}    AS estimated
            FROM "box-office-mojo-domestic-yearly"
            WHERE {_int('rank')} IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="box-office-mojo-worldwide-yearly-transform",
        deps=["box-office-mojo-worldwide-yearly"],
        sql=f'''
            SELECT
                CAST(year AS INTEGER)    AS year,
                {_int('rank')}           AS rank,
                release_group            AS release_group,
                {_money('worldwide')}    AS worldwide_gross,
                {_money('domestic')}     AS domestic_gross,
                {_pct('domestic_pct')}   AS domestic_pct,
                {_money('"foreign"')}    AS foreign_gross,
                {_pct('foreign_pct')}    AS foreign_pct
            FROM "box-office-mojo-worldwide-yearly"
            WHERE {_int('rank')} IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="box-office-mojo-weekend-summary-transform",
        deps=["box-office-mojo-weekend-summary"],
        sql=f'''
            SELECT
                CAST(year AS INTEGER)        AS year,
                {_int('week')}               AS week,
                {_bool('long_weekend')}      AS long_weekend,
                dates                        AS dates,
                {_money('top10_gross')}      AS top10_gross,
                {_pct('top10_change_pct')}   AS top10_change_pct,
                {_money('overall_gross')}    AS overall_gross,
                {_pct('overall_change_pct')} AS overall_change_pct,
                {_int('releases')}           AS releases,
                num1_release                 AS num1_release
            FROM "box-office-mojo-weekend-summary"
            WHERE {_int('week')} IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="box-office-mojo-domestic-weekend-transform",
        deps=["box-office-mojo-domestic-weekend"],
        sql=f'''
            SELECT
                weekend_id               AS weekend_id,
                CAST(year AS INTEGER)    AS year,
                {_int('week')}           AS week,
                {_int('rank')}           AS rank,
                {_int('last_week_rank')} AS last_week_rank,
                release                  AS release,
                {_money('gross')}        AS gross,
                {_pct('weekend_change_pct')} AS weekend_change_pct,
                {_int('theaters')}       AS theaters,
                {_sint('theater_change')} AS theater_change,
                {_money('average')}      AS average_per_theater,
                {_money('total_gross')}  AS total_gross,
                {_int('weeks')}          AS weeks_in_release,
                NULLIF(distributor, '-') AS distributor,
                {_bool('new_this_week')} AS new_this_week,
                {_bool('estimated')}     AS estimated
            FROM "box-office-mojo-domestic-weekend"
            WHERE {_int('rank')} IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="box-office-mojo-domestic-daily-transform",
        deps=["box-office-mojo-domestic-daily"],
        sql=f'''
            SELECT
                TRY_CAST(strptime(
                    regexp_extract(date_raw, '^[A-Za-z]{{3}} [0-9]{{1,2}}') || ' ' || year,
                    '%b %d %Y') AS DATE)     AS date,
                CAST(year AS INTEGER)        AS year,
                day_of_week                  AS day_of_week,
                {_int('day_num')}            AS day_of_year,
                {_money('top10_gross')}      AS top10_gross,
                {_pct('change_yd_pct')}      AS change_vs_yesterday_pct,
                {_pct('change_lw_pct')}      AS change_vs_last_week_pct,
                {_int('releases')}           AS releases,
                num1_release                 AS num1_release,
                {_money('gross')}            AS num1_gross
            FROM "box-office-mojo-domestic-daily"
            WHERE TRY_CAST(strptime(
                    regexp_extract(date_raw, '^[A-Za-z]{{3}} [0-9]{{1,2}}') || ' ' || year,
                    '%b %d %Y') AS DATE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="box-office-mojo-top-lifetime-grosses-transform",
        deps=["box-office-mojo-top-lifetime-grosses"],
        sql=f'''
            SELECT
                {_int('rank')}            AS rank,
                title                     AS title,
                {_money('lifetime_gross')} AS lifetime_gross,
                {_int('year')}            AS release_year
            FROM "box-office-mojo-top-lifetime-grosses"
            WHERE {_int('rank')} IS NOT NULL
        ''',
    ),
]
