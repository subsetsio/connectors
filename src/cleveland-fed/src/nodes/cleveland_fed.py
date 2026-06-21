"""Cleveland Fed connector — indicator data files behind the bank's
`indicators-and-data` pages.

Mechanism (research: `webcharts_csv`): every indicator page is backed by one or
more "webcharts" data files served from a stable, no-auth path
`https://www.clevelandfed.org/-/media/files/webcharts/<dir>/<file>`. Most are
tidy CSV time series (a leading date column + named numeric series); the
Inflation Nowcasting files are FusionCharts JSON payloads (x-axis labels +
per-series datasets). The site WAF 403s non-browser User-Agents, so every fetch
sends a browser UA.

Shape: stateless full re-pull. The whole corpus is a few MB of small files that
each carry their complete history, so every run re-downloads and overwrites —
no watermark, no cursor. Each fetch normalizes its file into a clean wide table
(snake_case numeric columns, a leading `date` ISO string for time-series files
or a `label` string for the nowcast files) and writes parquet; the SQL
transform casts `date` and publishes one Delta table per subset.
"""

import re
import csv
import io
import json
from datetime import datetime

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://www.clevelandfed.org/-/media/files/webcharts"
# The site WAF rejects non-browser agents (research: 403 otherwise). ASCII only.
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

# entity_id -> (webcharts subdir, filename, format). The exact accepted union
# (rank >= threshold); ids match the collect catalog keys verbatim.
CONFIG = {
    "crediteasing-fedagencydebtmbs": ("crediteasing", "fedagencydebtmbs.csv", "csv"),
    "crediteasing-lendingfincinst": ("crediteasing", "lendingfincinst.csv", "csv"),
    "crediteasing-liquiditykeymkts": ("crediteasing", "liquiditykeymkts.csv", "csv"),
    "crediteasing-longtermtreasuries": ("crediteasing", "longtermtreasuries.csv", "csv"),
    "crediteasing-summaryview": ("crediteasing", "summaryview.csv", "csv"),
    "crediteasing-tradsechold": ("crediteasing", "tradsechold.csv", "csv"),
    "inflationexpectations-inflationexpectations-chart1": ("inflationexpectations", "inflationexpectations_chart1.csv", "csv"),
    "inflationexpectations-inflationexpectations-chart2": ("inflationexpectations", "inflationexpectations_chart2.csv", "csv"),
    "inflationnowcasting-nowcast-month": ("inflationnowcasting", "nowcast_month.json", "json"),
    "inflationnowcasting-nowcast-quarter": ("inflationnowcasting", "nowcast_quarter.json", "json"),
    "inflationnowcasting-nowcast-year": ("inflationnowcasting", "nowcast_year.json", "json"),
    "mediancpi-core": ("mediancpi", "core.csv", "csv"),
    "mediancpi-cpi": ("mediancpi", "cpi.csv", "csv"),
    "mediancpi-mcpi-revised": ("mediancpi", "mcpi_revised.csv", "csv"),
    "mediancpi-mediancpi-chartdata": ("mediancpi", "mediancpi_chartdata.csv", "csv"),
    "mediancpi-trim-revised": ("mediancpi", "trim_revised.csv", "csv"),
    "medianpce-median-pce-full-history": ("medianpce", "median-pce-full-history.csv", "csv"),
    "medianpce-medianpce-chartdata": ("medianpce", "medianpce_chartdata.csv", "csv"),
    "policyrules-chartdata": ("policyrules", "chartdata.csv", "csv"),
    "sorce-sorce-web-data": ("sorce", "sorce_web_data.csv", "csv"),
    "survey-of-firms-survey-graph": ("survey_of_firms", "survey_graph.csv", "csv"),
    "systemicrisk-landing-systemicrisk": ("systemicrisk", "landing_systemicrisk.csv", "csv"),
    "yieldcurve-chart1-spread-vs-gdpgrowth-w-forecast": ("yieldcurve", "chart1_spread_vs_gdpgrowth_w_forecast.csv", "csv"),
    "yieldcurve-chart2-recession-probability-w-forecast": ("yieldcurve", "chart2_recession_probability_w_forecast.csv", "csv"),
    "yieldcurve-chart3-spread-vs-realgdp": ("yieldcurve", "chart3_spread_vs_realgdp.csv", "csv"),
    "yieldcurve-chart4-spread-vs-lagrealgdp": ("yieldcurve", "chart4_spread_vs_lagrealgdp.csv", "csv"),
}


@transient_retry()
def _fetch(url: str) -> bytes:
    resp = get(url, headers={"User-Agent": BROWSER_UA}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


_DATE_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATE_MDY = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{4})$")
_DATE_MY = re.compile(r"^(\d{1,2})/(\d{4})$")


def _parse_date(s: str):
    """Normalize the observed Cleveland Fed date formats to ISO 'YYYY-MM-DD'.
    Returns None when the cell is not a recognizable date."""
    s = (s or "").strip()
    if not s:
        return None
    if _DATE_ISO.match(s):
        return s
    m = _DATE_MDY.match(s)
    if m:
        mo, d, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{y:04d}-{mo:02d}-{d:02d}"
    m = _DATE_MY.match(s)
    if m:
        mo, y = int(m.group(1)), int(m.group(2))
        return f"{y:04d}-{mo:02d}-01"
    for fmt in ("%d%b%Y", "%b %Y", "%Y-%m"):
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def _to_float(s):
    if s is None:
        return None
    s = str(s).strip().replace(",", "").replace("%", "")
    if s == "" or s in ("-", "NA", "N/A", "null", "."):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _clean_col(name: str, used: set) -> str:
    base = re.sub(r"[^a-z0-9]+", "_", (name or "").lower()).strip("_") or "col"
    out = base
    i = 2
    while out in used:
        out = f"{base}_{i}"
        i += 1
    used.add(out)
    return out


def _save_wide(asset: str, key_name: str, key_type, key_values, value_cols, value_rows):
    """Write a wide table: a leading key column (date ISO string / label) plus
    one float64 column per series. Value columns that are entirely null in this
    file are dropped — some source files (e.g. the nowcast chart views) declare
    series placeholders they never populate, which would otherwise publish as
    all-null columns."""
    if not key_values:
        raise AssertionError(f"{asset}: parsed 0 rows from source file")
    kept = [c for c in value_cols if any(vals.get(c) is not None for vals in value_rows)]
    if not kept:
        raise AssertionError(f"{asset}: no populated value columns")
    schema = pa.schema([(key_name, key_type)] + [(c, pa.float64()) for c in kept])
    rows = []
    for k, vals in zip(key_values, value_rows):
        row = {key_name: k}
        row.update({c: vals.get(c) for c in kept})
        rows.append(row)
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, asset)


def _fetch_csv(asset: str, url: str) -> None:
    text = _fetch(url).decode("utf-8-sig", errors="replace")
    reader = csv.reader(io.StringIO(text))
    rows = [r for r in reader if r and any(c.strip() for c in r)]
    if len(rows) < 2:
        raise AssertionError(f"{asset}: CSV has no data rows")
    header = rows[0]
    used = set()
    value_cols = [_clean_col(h, used) for h in header[1:]]
    keys, value_rows = [], []
    for r in rows[1:]:
        keys.append(_parse_date(r[0]) or r[0].strip())
        cells = r[1:] + [None] * (len(value_cols) - len(r[1:]))
        value_rows.append({c: _to_float(cells[i]) for i, c in enumerate(value_cols)})
    _save_wide(asset, "date", pa.string(), keys, value_cols, value_rows)


def _fetch_nowcast_json(asset: str, url: str) -> None:
    doc = json.loads(_fetch(url).decode("utf-8-sig", errors="replace"))
    node = doc[0] if isinstance(doc, list) and doc else doc
    cats = node.get("categories") or []
    labels = [c.get("label", "") for c in (cats[0].get("category", []) if cats else [])]
    dataset = node.get("dataset") or []
    used = set()
    series_cols, series_data = [], []
    for d in dataset:
        name = d.get("seriesname") or d.get("seriesName") or "series"
        series_cols.append(_clean_col(name, used))
        series_data.append([_to_float((p or {}).get("value")) for p in d.get("data", [])])
    value_rows = []
    for i in range(len(labels)):
        value_rows.append({col: (data[i] if i < len(data) else None)
                           for col, data in zip(series_cols, series_data)})
    _save_wide(asset, "label", pa.string(), labels, series_cols, value_rows)


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity_id = node_id[len("cleveland-fed-"):]
    subdir, fname, fmt = CONFIG[entity_id]
    url = f"{BASE}/{subdir}/{fname}?sc_lang=en"
    if fmt == "json":
        _fetch_nowcast_json(asset, url)
    else:
        _fetch_csv(asset, url)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"cleveland-fed-{eid}", fn=fetch_one, kind="download")
    for eid in CONFIG
]


# Yield-curve files carry a `recession` column that is NOT a 0/1 flag — it holds
# chart y-axis band sentinels (e.g. -100 / +100 / 1000) used to shade recession
# bars on the source chart. A positive value marks a recession month; normalize
# to a clean 0/1 indicator so the published column means what its name says.
_RECESSION_BAND = {
    "yieldcurve-chart2-recession-probability-w-forecast",
    "yieldcurve-chart3-spread-vs-realgdp",
    "yieldcurve-chart4-spread-vs-lagrealgdp",
}


def _transform_sql(entity_id: str, download_id: str, fmt: str) -> str:
    if fmt == "json":
        # label-keyed nowcast: publish as-is (label + per-series values).
        return f'SELECT * FROM "{download_id}"'
    if entity_id in _RECESSION_BAND:
        # cast date, remap the recession band sentinel to 0/1, keep the rest.
        return (
            f'SELECT TRY_CAST(date AS DATE) AS date, '
            f'CASE WHEN recession > 0 THEN 1 ELSE 0 END AS recession, '
            f'* EXCLUDE (date, recession) FROM "{download_id}"'
        )
    # date-keyed time series: cast the leading date column, keep the rest.
    return f'SELECT TRY_CAST(date AS DATE) AS date, * EXCLUDE (date) FROM "{download_id}"'


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"cleveland-fed-{eid}-transform",
        deps=[f"cleveland-fed-{eid}"],
        sql=_transform_sql(eid, f"cleveland-fed-{eid}", fmt),
    )
    for eid, (_subdir, _fname, fmt) in CONFIG.items()
]
