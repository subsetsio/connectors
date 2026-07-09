"""Climatic Research Unit (UEA) connector.

Source: https://crudata.uea.ac.uk/cru/data/ (mechanism: crudata_bulk).
All entities are bulk ASCII files over stable HTTPS URLs; no auth, no API,
no incremental filter. Full re-pull every refresh (stateless) — the files are
small (KB-MB each) and the source revises in place, so a stored watermark would
only risk skipping corrections. The maintain step gates whether a fetch runs.

Two fetch shapes:

1. `fetch_temperature` — the 5 global/hemispheric temperature-anomaly products
   (HadCRUT5 Analysis & NonInfilled, CRUTEM5, CRUTEM5alt, HadSST4). Each is
   three region files (nh/sh/gl) in the CRU two-line text format: a value row
   (year + 12 monthly anomalies + annual) immediately followed by a station/
   coverage-count row (year + 12 monthly counts). Region folds into a column.
   Sentinel -9.999 = missing.

2. `fetch_country` — CRU CY country-level monthly climate (the `cru-cy-country`
   subset). For each of 10 variables it lists the per-country `.per` files in the
   current release directory and parses them into one long table
   (country, variable, unit, year, month, value). Sentinel -999.0 = missing.
   ~292 countries x 10 variables -> ~4M monthly rows, streamed per-variable.
"""

import re
from datetime import date

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    raw_parquet_writer,
)

SLUG = "climatic-research-unit"
TEMP_BASE = "https://crudata.uea.ac.uk/cru/data/temperature/"
HRG_BASE = "https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.09/"
REGIONS = ("nh", "sh", "gl")

# Per-spec filename template for the temperature products. {r} = region code.
# Region files share one schema, so each product is one download with `region`
# as a column.
TEMP_FILES = {
    f"{SLUG}-hadcrut5-analysis": "HadCRUT5.1Analysis_{r}.txt",
    f"{SLUG}-hadcrut5-noninfilled": "HadCRUT5.1NonInfilled_{r}.txt",
    f"{SLUG}-crutem5": "CRUTEM5.1_{r}.txt",
    f"{SLUG}-crutem5alt": "CRUTEM5.1alt_{r}.txt",
    f"{SLUG}-hadsst4": "HadSST4.2_{r}.txt",
}

# CRU TS / CY variables and their physical units (per CRU TS v4 documentation).
VAR_UNITS = {
    "cld": "percent",
    "dtr": "degC",
    "frs": "days",
    "pet": "mm/day",
    "pre": "mm/month",
    "tmn": "degC",
    "tmp": "degC",
    "tmx": "degC",
    "vap": "hPa",
    "wet": "days",
}

TEMP_MISSING = -9.999
CY_MISSING = -999.0
ABSOLUTE_URL = TEMP_BASE + "abs_glnhsh.txt"

# `date` (first-of-month) is carried on the RAW so the download-test freshness
# assertion has a real date column to read (year/month alone can't express a
# date-slack bound). The transforms recompute it from year/month, so the
# published schema is unchanged.
TEMP_SCHEMA = pa.schema([
    ("region", pa.string()),
    ("date", pa.date32()),
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("value", pa.float64()),
    ("station_count", pa.int32()),
])

CY_SCHEMA = pa.schema([
    ("country", pa.string()),
    ("variable", pa.string()),
    ("unit", pa.string()),
    ("date", pa.date32()),
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("value", pa.float64()),
])

ABSOLUTE_SCHEMA = pa.schema([
    ("region", pa.string()),
    ("month", pa.int32()),
    ("absolute_temperature_c", pa.float64()),
    ("anomaly_from_annual_mean_c", pa.float64()),
    ("annual_absolute_temperature_c", pa.float64()),
])

def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


# --- Temperature products --------------------------------------------------

def _parse_temperature(text: str):
    """CRU two-line text format. Returns rows of (year, month, value, count).

    Each year is a 14-token value row (year + 12 monthly + annual) immediately
    followed by a 13-token count row (year + 12 monthly counts). Missing values
    are -9.999; we emit them as None. The annual column (14th token) is dropped
    — it is derivable from the monthly values.
    """
    values = {}   # year -> [12 floats or None]
    counts = {}   # year -> [12 ints]
    for line in text.splitlines():
        toks = line.split()
        if len(toks) == 14:
            year = int(toks[0])
            values[year] = [
                None if abs(float(v) - TEMP_MISSING) < 1e-6 else float(v)
                for v in toks[1:13]
            ]
        elif len(toks) == 13:
            year = int(toks[0])
            counts[year] = [int(c) for c in toks[1:13]]
    rows = []
    for year in sorted(values):
        vals = values[year]
        cnts = counts.get(year, [None] * 12)
        for m in range(12):
            rows.append((year, m + 1, vals[m], cnts[m]))
    return rows


def fetch_temperature(node_id: str) -> None:
    asset = node_id
    template = TEMP_FILES[node_id]
    regions, dates, years, months, vals, cnts = [], [], [], [], [], []
    for region in REGIONS:
        url = TEMP_BASE + template.format(r=region)
        text = _get_text(url)
        parsed = _parse_temperature(text)
        if not parsed:
            raise AssertionError(f"{asset}: no rows parsed from {url}")
        for year, month, value, count in parsed:
            regions.append(region)
            dates.append(date(year, month, 1))
            years.append(year)
            months.append(month)
            vals.append(value)
            cnts.append(count)
    table = pa.table(
        {
            "region": regions,
            "date": dates,
            "year": years,
            "month": months,
            "value": vals,
            "station_count": cnts,
        },
        schema=TEMP_SCHEMA,
    )
    save_raw_parquet(table, asset)


# --- Country-level CRU CY --------------------------------------------------

def _resolve_crucy_dir() -> str:
    """Resolve the current timestamped crucy.* release directory (the build
    timestamp changes per release, so it must be discovered, not hardcoded)."""
    text = _get_text(HRG_BASE)
    dirs = re.findall(r'href="(crucy\.[^"/]+)"', text)
    if not dirs:
        raise AssertionError(f"no crucy.* release dir found under {HRG_BASE}")
    return HRG_BASE + dirs[0] + "/countries/"


def _list_per_files(var_dir: str):
    text = _get_text(var_dir)
    return re.findall(r'href="([^"]+\.per)"', text)


def _parse_country_file(text: str, variable: str):
    """Parse one CRU CY `.per` file. Header lines then data rows of
    year + 12 monthly + 4 seasonal + annual (18 tokens). Returns
    (country, rows[(year, month, value)]). Missing value is -999.0 -> None."""
    country = None
    rows = []
    for line in text.splitlines():
        if country is None:
            m = re.search(r"Country\s*=\s*(\S+)", line)
            if m:
                country = m.group(1).replace("_", " ")
            continue
        toks = line.split()
        # data rows: year + 17 numeric columns; skip the YEAR/JAN/... header.
        if len(toks) >= 13 and toks[0].isdigit():
            year = int(toks[0])
            for m_idx in range(12):
                raw = float(toks[1 + m_idx])
                value = None if abs(raw - CY_MISSING) < 1e-6 else raw
                rows.append((year, m_idx + 1, value))
    if country is None:
        raise AssertionError(f"{variable}: could not parse Country from header")
    return country, rows


def fetch_country(node_id: str) -> None:
    asset = node_id
    countries_dir = _resolve_crucy_dir()
    with raw_parquet_writer(asset, CY_SCHEMA) as writer:
        for variable, unit in VAR_UNITS.items():
            var_dir = countries_dir + variable + "/"
            files = _list_per_files(var_dir)
            if not files:
                raise AssertionError(f"{asset}: no .per files for variable {variable} at {var_dir}")
            v_country, v_var, v_unit, v_date, v_year, v_month, v_value = [], [], [], [], [], [], []
            for fname in files:
                text = _get_text(var_dir + fname)
                country, rows = _parse_country_file(text, variable)
                for year, month, value in rows:
                    v_country.append(country)
                    v_var.append(variable)
                    v_unit.append(unit)
                    v_date.append(date(year, month, 1))
                    v_year.append(year)
                    v_month.append(month)
                    v_value.append(value)
            batch = pa.table(
                {
                    "country": v_country,
                    "variable": v_var,
                    "unit": v_unit,
                    "date": v_date,
                    "year": v_year,
                    "month": v_month,
                    "value": v_value,
                },
                schema=CY_SCHEMA,
            )
            writer.write_table(batch)


def fetch_absolute(node_id: str) -> None:
    text = _get_text(ABSOLUTE_URL)
    annual = {}
    rows = []
    for line in text.splitlines():
        toks = line.split()
        if len(toks) == 4 and toks[0] == "Annual":
            annual = {
                "gl": float(toks[1]),
                "nh": float(toks[2]),
                "sh": float(toks[3]),
            }
            continue
        if len(toks) == 8 and toks[0].isdigit():
            month = int(toks[0])
            rows.extend([
                ("gl", month, float(toks[2]), float(toks[3])),
                ("nh", month, float(toks[4]), float(toks[5])),
                ("sh", month, float(toks[6]), float(toks[7])),
            ])
    if len(rows) != 36 or set(annual) != set(REGIONS):
        raise AssertionError(f"{node_id}: expected 36 monthly rows and 3 annual values")
    table = pa.table(
        {
            "region": [r[0] for r in rows],
            "month": [r[1] for r in rows],
            "absolute_temperature_c": [r[2] for r in rows],
            "anomaly_from_annual_mean_c": [r[3] for r in rows],
            "annual_absolute_temperature_c": [annual[r[0]] for r in rows],
        },
        schema=ABSOLUTE_SCHEMA,
    )
    save_raw_parquet(table, node_id)


# --- Specs -----------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id=sid, fn=fetch_temperature, kind="download")
    for sid in TEMP_FILES
] + [
    NodeSpec(id=f"{SLUG}-cru-cy-country", fn=fetch_country, kind="download"),
    NodeSpec(id=f"{SLUG}-absolute-temperatures", fn=fetch_absolute, kind="download"),
]
