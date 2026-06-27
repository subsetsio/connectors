"""Lincoln Institute of Land Policy connector.

Three independent products, three fetch mechanisms, six published subsets:

1. **Atlas of Urban Expansion** (atlasofurbanexpansion.org) — static 2016 bulk
   CSVs with a two-row (metric-group / period) header covering the global
   ~200-city sample. Fetched over plain HTTP via ``subsets_utils.get`` and
   flattened into a tidy (city x metric x period) long table.
       - atlas-areas-and-densities
       - atlas-blocks-and-roads-1

2. **Fiscally Standardized Cities (FiSC)** — POST app.lincolninst.edu/fisc/api/results.
   One request per central city (``orderby=City`` + all years + all finance
   categories) returns that city's full year x category matrix, melted to long.
       - fisc-values

3. **State-by-State Property Tax at a Glance** — POST
   app.lincolninst.edu/property-tax-data-visualization/json with ``year=YYYY``.
   Three tables per year; each is published as its own state x year long subset.
       - glance-sources-of-local-general-revenue  (numeric, % shares)
       - glance-selected-property-tax-statistics  (numeric, $/%/rank)
       - glance-property-tax-features             (categorical Yes/No flags)

Fetch shape: **stateless full re-pull** for all six. The whole corpus is a few
MB (Atlas frozen snapshot; FiSC ~212 cities; Glance ~9 data years) and re-fetches
in a few minutes — no incremental filter exists on any product, so we always
pull the full corpus and overwrite.

WAF note: ``app.lincolninst.edu`` sits behind a WAF that rejects the stdlib
TLS/JA3 fingerprint used by ``subsets_utils.get/post`` (httpx) with a blanket
HTTP 403 — verified from multiple networks; a real browser TLS handshake returns
200. We therefore reach the FiSC and Glance endpoints through ``curl_cffi`` with
Chrome TLS impersonation (the only client that gets past the WAF). Atlas lives on
a different host and is fetched normally through ``subsets_utils.get``.
"""
import html as _html
import re
from datetime import datetime, timezone

import pyarrow as pa
from curl_cffi import requests as _curl
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    save_raw_parquet,
)

# --------------------------------------------------------------------------- #
# Shared parsing helpers
# --------------------------------------------------------------------------- #

_NULLISH = {"", "-", "–", "—", "n/a", "na", "..", ".", "#n/a", "null", "none"}


def _parse_num(v):
    """Parse a source value to float, or None. Handles thousands separators,
    a trailing percent sign, surrounding whitespace, and null sentinels."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if s.lower() in _NULLISH:
        return None
    pct = s.endswith("%")
    s = s.replace("%", "").replace(",", "").strip()
    if s.lower() in _NULLISH:
        return None
    try:
        x = float(s)
    except ValueError:
        return None
    return x / 100.0 if pct else x


def _clean_str(v):
    """Normalise a categorical value: strip, map null sentinels to None."""
    if v is None:
        return None
    s = str(v).strip()
    return None if s.lower() in _NULLISH else s


# --------------------------------------------------------------------------- #
# Atlas of Urban Expansion — bulk CSV (plain HTTP, two-row header)
# --------------------------------------------------------------------------- #

# Atlas is served over plain HTTP only; the host presents an invalid TLS record
# on :443 (SSL WRONG_VERSION_NUMBER) so https is impossible. Static 2016 snapshot.
_ATLAS_BASE = "http://atlasofurbanexpansion.org/file-manager/userfiles/data_page"

_ATLAS_FILES = {
    "lincoln-institute-atlas-areas-and-densities":
        "Areas_and_Densities_Tables/Areas_and_Densities_Table_1.csv",
    "lincoln-institute-atlas-blocks-and-roads-1":
        "Blocks_and_Roads_Tables/Blocks_and_Roads_Table_1.csv",
}

# Leading metric-group labels that are row identity, not melted metrics.
_ATLAS_IDENTITY_GROUPS = {"City Name", "Country", "Region", "CBD Location"}
# Metric group carrying the per-period observation dates — context, not a metric.
_ATLAS_DROP_GROUPS = {"Land Cover Dates"}

_ATLAS_SCHEMA = pa.schema([
    ("city", pa.string()),
    ("country", pa.string()),
    ("region", pa.string()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("metric", pa.string()),
    ("period", pa.string()),
    ("value", pa.float64()),
])


@retry(
    retry=retry_if_exception_type(Exception),
    stop=stop_after_attempt(6),
    wait=wait_exponential(multiplier=2, min=4, max=120),
    reraise=True,
)
def _atlas_csv(url):
    import csv
    import io
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    text = resp.content.decode("utf-8-sig", errors="replace")
    return list(csv.reader(io.StringIO(text)))


def fetch_atlas(node_id):
    """Download one Atlas combined CSV and flatten the two-row header into a
    tidy (city, metric, period, value) long table."""
    asset = node_id
    rel = _ATLAS_FILES[node_id]
    rows = _atlas_csv(f"{_ATLAS_BASE}/{rel}")
    if len(rows) < 3:
        raise AssertionError(f"{asset}: expected a header + data rows, got {len(rows)}")

    # Forward-fill the merged metric-group header row; second row is the period.
    group_row, period_row = rows[0], rows[1]
    groups, cur = [], ""
    for cell in group_row:
        c = cell.strip()
        if c:
            cur = c
        groups.append(cur)
    periods = [c.strip() for c in period_row]
    width = len(groups)

    # Map identity columns by (group, period-subheader).
    col_lat = col_lon = None
    metric_cols = []  # (idx, metric, period)
    for i in range(width):
        g = groups[i] if i < len(groups) else ""
        p = periods[i] if i < len(periods) else ""
        if g == "CBD Location":
            if p == "Latitude":
                col_lat = i
            elif p == "Longitude":
                col_lon = i
        elif g in _ATLAS_IDENTITY_GROUPS or g in _ATLAS_DROP_GROUPS or not g:
            continue
        else:
            metric_cols.append((i, g, p))

    out = {k: [] for k in _ATLAS_SCHEMA.names}
    for r in rows[2:]:
        if not r or not r[0].strip():
            continue  # blank separator / trailing rows
        city = r[0].strip()
        country = r[1].strip() if len(r) > 1 else None
        region = r[2].strip() if len(r) > 2 else None
        lat = _parse_num(r[col_lat]) if col_lat is not None and col_lat < len(r) else None
        lon = _parse_num(r[col_lon]) if col_lon is not None and col_lon < len(r) else None
        for idx, metric, period in metric_cols:
            if idx >= len(r):
                continue
            val = _parse_num(r[idx])
            if val is None:
                continue
            out["city"].append(city)
            out["country"].append(country)
            out["region"].append(region)
            out["latitude"].append(lat)
            out["longitude"].append(lon)
            out["metric"].append(metric)
            out["period"].append(period)
            out["value"].append(val)

    table = pa.table({k: pa.array(out[k], type=_ATLAS_SCHEMA.field(k).type)
                      for k in _ATLAS_SCHEMA.names}, schema=_ATLAS_SCHEMA)
    if table.num_rows == 0:
        raise AssertionError(f"{asset}: flattened to 0 rows")
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# WAF-protected app.lincolninst.edu — curl_cffi (Chrome TLS impersonation)
# --------------------------------------------------------------------------- #

_IMPERSONATE = "chrome"


@retry(
    retry=retry_if_exception_type(Exception),
    stop=stop_after_attempt(6),
    wait=wait_exponential(multiplier=2, min=4, max=120),
    reraise=True,
)
def _waf_get(url):
    r = _curl.get(url, impersonate=_IMPERSONATE, timeout=120)
    r.raise_for_status()
    return r


@retry(
    retry=retry_if_exception_type(Exception),
    stop=stop_after_attempt(6),
    wait=wait_exponential(multiplier=2, min=4, max=120),
    reraise=True,
)
def _waf_post(url, data):
    r = _curl.post(url, data=data, impersonate=_IMPERSONATE, timeout=120)
    r.raise_for_status()
    return r


# --------------------------------------------------------------------------- #
# FiSC — Fiscally Standardized Cities
# --------------------------------------------------------------------------- #

_FISC_SEARCH = ("https://app.lincolninst.edu/research-data/data-toolkits/"
                "fiscally-standardized-cities/search-database")
_FISC_API = "https://app.lincolninst.edu/fisc/api/results"
# A real central city option is "ST: City"; aggregate rows are "Average .."/"Median ..".
_FISC_CITY_RE = re.compile(r"^[A-Z]{2}:\s")

_FISC_SCHEMA = pa.schema([
    ("city", pa.string()),
    ("state", pa.string()),
    ("year", pa.int32()),
    ("category", pa.string()),
    ("value", pa.float64()),
])


def _fisc_options(field, page_html):
    """Extract the value="..." list for an <input name="field"> set."""
    out = []
    for m in re.finditer(r'<input[^>]*\bname="' + re.escape(field) + r'"[^>]*>', page_html):
        v = re.search(r'\bvalue="([^"]*)"', m.group(0))
        if v:
            out.append(_html.unescape(v.group(1)))
    return out


def fetch_fisc(node_id):
    """Fetch the FiSC corpus: one POST per real central city returns that city's
    full year x finance-category matrix, melted to long (city, state, year,
    category, value). City/year/category option sets are discovered live from the
    search page so new cities/years/categories are picked up automatically."""
    asset = node_id
    page = _waf_get(_FISC_SEARCH).text
    cities = [c for c in _fisc_options("cities[]", page) if _FISC_CITY_RE.match(c)]
    years = _fisc_options("years[]", page)
    revenues = _fisc_options("revenues[]", page)
    expendchar = _fisc_options("expendchar[]", page)
    debts = _fisc_options("debts[]", page)
    if not cities or not years or not revenues:
        raise AssertionError(
            f"{asset}: search-page enumeration failed "
            f"(cities={len(cities)} years={len(years)} revenues={len(revenues)})")

    base = [("levelofgov[]", "fisc"), ("units", "Total"),
            ("inflation", "Nominal"), ("orderby", "City")]
    base += [("years[]", y) for y in years]
    base += [("revenues[]", c) for c in revenues]
    base += [("expendchar[]", c) for c in expendchar]
    base += [("debts[]", c) for c in debts]

    with raw_parquet_writer(asset, _FISC_SCHEMA) as w:
        for city in cities:
            state = city.split(":", 1)[0].strip()
            data = _waf_post(_FISC_API, [("cities[]", city)] + base).json()
            table = data.get("table") or []
            if len(table) < 2:
                continue  # no observations for this city
            header = table[0]
            categories = header[1:]  # header[0] == "Year"
            cols = {k: [] for k in _FISC_SCHEMA.names}
            for row in table[1:]:
                try:
                    year = int(str(row[0]).strip())
                except (ValueError, IndexError):
                    continue
                for j, cat in enumerate(categories, start=1):
                    if j >= len(row):
                        continue
                    val = _parse_num(row[j])
                    if val is None:
                        continue
                    cols["city"].append(city)
                    cols["state"].append(state)
                    cols["year"].append(year)
                    cols["category"].append(cat)
                    cols["value"].append(val)
            if not cols["year"]:
                continue
            batch = pa.table(
                {k: pa.array(cols[k], type=_FISC_SCHEMA.field(k).type)
                 for k in _FISC_SCHEMA.names},
                schema=_FISC_SCHEMA,
            )
            w.write_table(batch)


# --------------------------------------------------------------------------- #
# Property Tax at a Glance
# --------------------------------------------------------------------------- #

_GLANCE_API = "https://app.lincolninst.edu/property-tax-data-visualization/json"
# Earliest plausible era to probe forward from; the tool only began publishing
# structured data in the 2010s (current observed span ~2013-2022, with gaps).
_GLANCE_MIN_YEAR = 2005

# node id -> (TableID in the JSON response, value kind)
_GLANCE_TABLES = {
    "lincoln-institute-glance-sources-of-local-general-revenue": ("figure_1", "numeric"),
    "lincoln-institute-glance-selected-property-tax-statistics": ("table_1", "numeric"),
    "lincoln-institute-glance-property-tax-features": ("table_2", "string"),
}

_GLANCE_NUM_SCHEMA = pa.schema([
    ("state", pa.string()),
    ("year", pa.int32()),
    ("metric", pa.string()),
    ("value", pa.float64()),
])
_GLANCE_STR_SCHEMA = pa.schema([
    ("state", pa.string()),
    ("year", pa.int32()),
    ("metric", pa.string()),
    ("value", pa.string()),
])


def _glance_year(year):
    """POST one year; return the list-of-tables payload (or [] if the year has
    no published data — the tool answers 200 with an empty body for those)."""
    r = _waf_post(_GLANCE_API, {"year": str(year)})
    try:
        data = r.json()
    except Exception:
        return []
    if not isinstance(data, list):
        return []
    return data


def fetch_glance(node_id):
    """Fetch one of the three Glance tables across every year that has data.
    Years are discovered by probing forward from a floor to the current year and
    keeping the non-empty ones (no list endpoint exists; the span has gaps)."""
    asset = node_id
    table_id, kind = _GLANCE_TABLES[node_id]
    numeric = kind == "numeric"
    schema = _GLANCE_NUM_SCHEMA if numeric else _GLANCE_STR_SCHEMA

    this_year = datetime.now(tz=timezone.utc).year
    cols = {k: [] for k in schema.names}
    found_any = False
    for year in range(_GLANCE_MIN_YEAR, this_year + 1):
        tables = _glance_year(year)
        target = next((t for t in tables if t.get("TableID") == table_id), None)
        if not target:
            continue
        items = target.get("TableDataItems") or []
        year_rows = 0
        for item in items:
            metric = _clean_str(item.get("RowName"))
            for rd in item.get("RowData") or []:
                state = _clean_str(rd.get("State"))
                if state is None:
                    continue
                raw_val = rd.get("Value")
                value = _parse_num(raw_val) if numeric else _clean_str(raw_val)
                if value is None:
                    continue
                cols["state"].append(state)
                cols["year"].append(year)
                cols["metric"].append(metric)
                cols["value"].append(value)
                year_rows += 1
        if year_rows:
            found_any = True

    if not found_any:
        raise AssertionError(f"{asset}: no Glance data found for table {table_id}")
    table = pa.table(
        {k: pa.array(cols[k], type=schema.field(k).type) for k in schema.names},
        schema=schema,
    )
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# DOWNLOAD_SPECS — one per entity-union entry
# --------------------------------------------------------------------------- #

DOWNLOAD_SPECS = [
    NodeSpec(id="lincoln-institute-atlas-areas-and-densities", fn=fetch_atlas, kind="download"),
    NodeSpec(id="lincoln-institute-atlas-blocks-and-roads-1", fn=fetch_atlas, kind="download"),
    NodeSpec(id="lincoln-institute-fisc-values", fn=fetch_fisc, kind="download"),
    NodeSpec(id="lincoln-institute-glance-property-tax-features", fn=fetch_glance, kind="download"),
    NodeSpec(id="lincoln-institute-glance-selected-property-tax-statistics", fn=fetch_glance, kind="download"),
    NodeSpec(id="lincoln-institute-glance-sources-of-local-general-revenue", fn=fetch_glance, kind="download"),
]


# --------------------------------------------------------------------------- #
# TRANSFORM_SPECS — one published Delta table per subset (thin parse-and-type)
# --------------------------------------------------------------------------- #

_ATLAS_SQL = '''
    SELECT city, country, region, latitude, longitude, metric, period,
           CAST(value AS DOUBLE) AS value
    FROM "{dep}"
    WHERE value IS NOT NULL
'''

_FISC_SQL = '''
    SELECT city, state, CAST(year AS INTEGER) AS year, category,
           CAST(value AS DOUBLE) AS value
    FROM "{dep}"
    WHERE value IS NOT NULL
'''

_GLANCE_NUM_SQL = '''
    SELECT state, CAST(year AS INTEGER) AS year, metric,
           CAST(value AS DOUBLE) AS value
    FROM "{dep}"
    WHERE value IS NOT NULL
'''

_GLANCE_STR_SQL = '''
    SELECT state, CAST(year AS INTEGER) AS year, metric, value
    FROM "{dep}"
    WHERE value IS NOT NULL
'''

_TRANSFORM_SQL = {
    "lincoln-institute-atlas-areas-and-densities": _ATLAS_SQL,
    "lincoln-institute-atlas-blocks-and-roads-1": _ATLAS_SQL,
    "lincoln-institute-fisc-values": _FISC_SQL,
    "lincoln-institute-glance-sources-of-local-general-revenue": _GLANCE_NUM_SQL,
    "lincoln-institute-glance-selected-property-tax-statistics": _GLANCE_NUM_SQL,
    "lincoln-institute-glance-property-tax-features": _GLANCE_STR_SQL,
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_TRANSFORM_SQL[s.id].format(dep=s.id),
    )
    for s in DOWNLOAD_SPECS
]
