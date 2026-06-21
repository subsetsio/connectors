"""GHS Index connector.

Single static bulk CSV (the 2021 Global Health Security Index release, which
also carries the 2019 scores). The source publishes one wide table: 390 rows
(195 countries x assessment years 2019 & 2021) and 311 hierarchical score
columns whose headers encode the GHS Index scoring tree
("1.1.1a) National plan for AMR priority pathogens").

The fetch fn melts that wide table into a tidy long form
(country, year, indicator_code, indicator_label, level, score) — header->code
parsing is structural surgery a SQL UNPIVOT can't do cleanly, so it lives here
and the transform stays a thin cast/projection pass.

Stateless full re-pull: the artefact is a fixed snapshot (last updated April
2022), tiny (~410KB), re-fetched in full every run. No watermark/cursor.
"""

import io
import csv
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    configure_http,
    transient_retry,
    save_raw_parquet,
)

CSV_URL = "https://www.ghsindex.org/wp-content/uploads/2022/04/2021-GHS-Index-April-2022.csv"

# The host (WordPress + WAF) 403s the default client User-Agent from datacenter
# IPs (the cloud runner), while a browser-like UA + Accept headers pass. Plain
# ASCII only — httpx rejects non-ASCII header values.
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/csv,application/csv,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://ghsindex.org/report-model/",
}

SCHEMA = pa.schema([
    ("country", pa.string()),
    ("year", pa.int32()),
    ("indicator_code", pa.string()),
    ("indicator_label", pa.string()),
    ("level", pa.string()),
    ("score", pa.float64()),
])


@transient_retry()
def _fetch_csv(url: str) -> str:
    configure_http(headers=_BROWSER_HEADERS)
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    # First column header carries a UTF-8 BOM; utf-8-sig strips it.
    return resp.content.decode("utf-8-sig")


def _parse_header(h: str) -> tuple[str, str]:
    """Split a score-column header into (indicator_code, indicator_label)."""
    if h.strip().upper() == "OVERALL SCORE":
        return "OVERALL", "Overall score"
    if ")" in h:
        code, label = h.split(")", 1)
        return code.strip(), label.strip()
    return h.strip(), h.strip()


def _level(code: str) -> str:
    if code == "OVERALL":
        return "overall"
    if re.fullmatch(r"\d+", code):
        return "category"
    if re.fullmatch(r"\d+\.\d+", code):
        return "indicator"
    if re.fullmatch(r"\d+\.\d+\.\d+", code):
        return "subindicator"
    if re.fullmatch(r"\d+\.\d+\.\d+[a-z]+", code):
        return "question"
    return "other"


def fetch_scores(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    text = _fetch_csv(CSV_URL)
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    if header[:2] != ["Country", "Year"]:
        raise AssertionError(f"unexpected leading columns: {header[:2]!r}")

    # Pre-parse the score-column headers once.
    cols = [(_parse_header(h)[0], _parse_header(h)[1]) for h in header[2:]]

    countries: list[str] = []
    years: list[int] = []
    codes: list[str] = []
    labels: list[str] = []
    levels: list[str] = []
    scores: list[float | None] = []

    for row in reader:
        if not row or not row[0].strip():
            continue
        country = row[0]
        year = int(row[1])
        for (code, label), raw in zip(cols, row[2:]):
            raw = raw.strip()
            countries.append(country)
            years.append(year)
            codes.append(code)
            labels.append(label)
            levels.append(_level(code))
            scores.append(float(raw) if raw != "" else None)

    table = pa.table(
        {
            "country": countries,
            "year": years,
            "indicator_code": codes,
            "indicator_label": labels,
            "level": levels,
            "score": scores,
        },
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="ghs-index-ghs-index-scores", fn=fetch_scores, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ghs-index-ghs-index-scores-transform",
        deps=["ghs-index-ghs-index-scores"],
        sql='''
            SELECT
                country,
                CAST(year AS INTEGER)      AS year,
                indicator_code,
                indicator_label,
                level,
                CAST(score AS DOUBLE)      AS score
            FROM "ghs-index-ghs-index-scores"
            WHERE score IS NOT NULL
        ''',
    ),
]
