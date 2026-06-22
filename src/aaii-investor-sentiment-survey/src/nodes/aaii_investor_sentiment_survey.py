"""AAII Investor Sentiment Survey connector.

Single-dataset source: the whole connector is one weekly time series (bullish /
neutral / bearish share of surveyed individual investors, 1987-present) delivered
as ONE legacy .xls file (sheet 'SENTIMENT') — one publishable subset.

Fetch shape: stateless full re-pull (shape 1). The corpus is a single ~1.1MB file
that carries the entire history, so we re-fetch and overwrite every run; revisions
and late corrections are picked up for free. No state, no watermark.

Transport: aaii.com is behind an Imperva/Incapsula bot wall — a plain GET returns
HTTP 403 with a JS sensor challenge we cannot solve. We therefore attempt the direct
URL first (in case the runner IP is allow-listed / un-challenged) and fall back to
the Internet Archive Wayback Machine, which keeps a status-200 snapshot of this exact
file (re-crawled every few weeks; lags the live source by days-to-weeks). The raw
.xls is binary so SQL cannot read it — the fetch fn parses it to a clean parquet and
the SQL transform does the thin type/rename/null-drop pass.
"""

import io

import pyarrow as pa
import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

DIRECT_URL = "https://www.aaii.com/files/surveys/sentiment.xls"
WAYBACK_AVAILABLE = "https://archive.org/wayback/available?url=aaii.com/files/surveys/sentiment.xls"
DATA_SHEET = "SENTIMENT"

# Sheet layout (verified by probing): a multi-row header; the usable column header
# is the 4th row (0-indexed 3), the next row (index 4) is blank, weekly data begins
# at index 5. Columns in source order — the trailing 14th column is junk and dropped.
RAW_COLUMNS = [
    "date",                       # reported (Wednesday) date
    "bullish",                    # share bullish (fraction 0..1)
    "neutral",                    # share neutral
    "bearish",                    # share bearish
    "total",                      # bullish+neutral+bearish (~1.0)
    "bullish_8wk_mov_avg",        # 8-week moving average of bullish
    "bull_bear_spread",           # bullish - bearish
    "bullish_average",            # long-run mean of bullish (constant column)
    "bullish_avg_plus_stdev",     # long-run mean + 1 std dev
    "bullish_avg_minus_stdev",    # long-run mean - 1 std dev
    "sp500_weekly_high",          # S&P 500 weekly high
    "sp500_weekly_low",           # S&P 500 weekly low
    "sp500_weekly_close",         # S&P 500 weekly close
]

RAW_SCHEMA = pa.schema(
    [("date", pa.date32())] + [(c, pa.float64()) for c in RAW_COLUMNS[1:]]
)


@transient_retry()
def _http_get(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _looks_like_xls(content: bytes) -> bool:
    # OLE2 / Composite Document File magic number for legacy .xls.
    return content[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


def _download_xls() -> bytes:
    """Return the raw .xls bytes, trying the live URL first then Wayback."""
    # 1) Direct — works only if the runner IP is not Incapsula-challenged.
    try:
        resp = _http_get(DIRECT_URL)
        if _looks_like_xls(resp.content):
            return resp.content
        print(f"direct fetch returned non-xls ({len(resp.content)} bytes, "
              f"ctype={resp.headers.get('content-type')}); falling back to Wayback")
    except Exception as exc:  # noqa: BLE001 - logged, then we fall back to Wayback
        print(f"direct fetch failed ({type(exc).__name__}: {exc}); falling back to Wayback")

    # 2) Wayback Machine — verified no-challenge transport.
    snap = _http_get(WAYBACK_AVAILABLE).json()["archived_snapshots"].get("closest")
    if not snap or snap.get("status") != "200":
        raise RuntimeError(f"no usable Wayback snapshot for {DIRECT_URL}: {snap}")
    raw_url = f"https://web.archive.org/web/{snap['timestamp']}id_/{DIRECT_URL}"
    content = _http_get(raw_url).content
    if not _looks_like_xls(content):
        raise RuntimeError(
            f"Wayback snapshot {snap['timestamp']} did not return a legacy .xls "
            f"({len(content)} bytes, magic={content[:8]!r})"
        )
    return content


def fetch_sentiment(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    content = _download_xls()
    df = pd.read_excel(
        io.BytesIO(content), sheet_name=DATA_SHEET, header=3, skiprows=[4], engine="xlrd"
    )

    # Guard the layout: the parsed frame must start with the Date column and carry
    # the 13 data columns plus a trailing junk column. If AAII reshapes the sheet
    # this trips loudly instead of publishing garbage.
    if df.shape[1] < len(RAW_COLUMNS):
        raise AssertionError(f"unexpected sheet shape {df.shape}; columns={list(df.columns)}")

    df = df.iloc[:, : len(RAW_COLUMNS)].copy()
    df.columns = RAW_COLUMNS

    # Drop the ~206 trailing footer rows (annual 'Count'/'Average' summaries): keep
    # only rows whose Date cell parses as a real date.
    parsed_date = pd.to_datetime(df["date"], errors="coerce")
    df = df[parsed_date.notna()].copy()
    df["date"] = parsed_date[parsed_date.notna()].dt.date

    for col in RAW_COLUMNS[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if len(df) < 1500:
        raise AssertionError(f"only {len(df)} weekly rows parsed; expected >=1500 (1987-present)")

    table = pa.Table.from_pandas(df, schema=RAW_SCHEMA, preserve_index=False)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="aaii-investor-sentiment-survey-investor-sentiment-survey-weekly",
        fn=fetch_sentiment,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(date AS DATE)                  AS date,
                CAST(bullish AS DOUBLE)             AS bullish,
                CAST(neutral AS DOUBLE)             AS neutral,
                CAST(bearish AS DOUBLE)             AS bearish,
                CAST(total AS DOUBLE)               AS total,
                CAST(bullish_8wk_mov_avg AS DOUBLE) AS bullish_8wk_mov_avg,
                CAST(bull_bear_spread AS DOUBLE)    AS bull_bear_spread,
                CAST(bullish_average AS DOUBLE)     AS bullish_average,
                CAST(bullish_avg_plus_stdev AS DOUBLE)  AS bullish_avg_plus_stdev,
                CAST(bullish_avg_minus_stdev AS DOUBLE) AS bullish_avg_minus_stdev,
                CAST(sp500_weekly_high AS DOUBLE)   AS sp500_weekly_high,
                CAST(sp500_weekly_low AS DOUBLE)    AS sp500_weekly_low,
                CAST(sp500_weekly_close AS DOUBLE)  AS sp500_weekly_close
            FROM "{s.id}"
            WHERE date IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
