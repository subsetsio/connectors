"""Berkeley Earth temperature-timeseries subset — long-format monthly anomalies.

Global products (land TAVG/TMAX/TMIN and the flagship land+ocean TAVG) come from
the S3 bucket; ~7 continents, ~153 countries and ~49 US states come from the
data.berkeleyearth.org /auto archive, each x {TAVG, TMAX, TMIN}. Every file is the
same commented-header fixed-column ASCII "Trend" layout, so they merge into one
table. Files are overwritten in place on each ~monthly release with stable
filenames, so we re-pull the full corpus every run (a few MB of text).
"""
from __future__ import annotations

import concurrent.futures as cf

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import BASE_S3, fetch_text

# --------------------------------------------------------------------------- #
# Sources
# --------------------------------------------------------------------------- #
BASE_AUTO = "https://data.berkeleyearth.org/auto/"
VARIABLES = ("TAVG", "TMAX", "TMIN")

# Global text products on S3 (Global/<file>): (filename, variable, surface).
GLOBAL_PRODUCTS = (
    ("Land_and_Ocean_complete.txt", "TAVG", "land_ocean"),
    ("Complete_TAVG_complete.txt", "TAVG", "land"),
    ("Complete_TMAX_complete.txt", "TMAX", "land"),
    ("Complete_TMIN_complete.txt", "TMIN", "land"),
)

# Region slugs verified live against /auto/Regional/TAVG/Text/ (all 200/206).
# Slug = lowercased-hyphenated region name; the archive serves countries and US
# states in the same namespace, so "georgia" resolves to the country (Republic of
# Georgia) and is listed once — the US state georgia is not separately reachable.
_CONTINENTS = (
    "africa", "asia", "europe", "north-america", "south-america", "oceania",
    "antarctica",
)
_COUNTRIES = (
    "afghanistan", "albania", "algeria", "angola", "argentina", "armenia",
    "australia", "austria", "azerbaijan", "bangladesh", "belarus", "belgium",
    "belize", "benin", "bhutan", "bolivia", "bosnia-and-herzegovina", "botswana",
    "brazil", "bulgaria", "burkina-faso", "burma", "burundi", "cambodia",
    "cameroon", "canada", "chad", "chile", "china", "colombia", "congo",
    "costa-rica", "croatia", "cuba", "cyprus", "czech-republic", "denmark",
    "dominican-republic", "ecuador", "egypt", "el-salvador", "eritrea", "estonia",
    "ethiopia", "finland", "france", "gabon", "georgia", "germany", "ghana",
    "greece", "greenland", "guatemala", "guinea", "guyana", "haiti", "honduras",
    "hungary", "iceland", "india", "indonesia", "iran", "iraq", "ireland",
    "israel", "italy", "ivory-coast", "jamaica", "japan", "jordan", "kazakhstan",
    "kenya", "kuwait", "kyrgyzstan", "laos", "latvia", "lebanon", "lesotho",
    "liberia", "libya", "lithuania", "luxembourg", "macedonia", "madagascar",
    "malawi", "malaysia", "mali", "mauritania", "mexico", "moldova", "mongolia",
    "montenegro", "morocco", "mozambique", "namibia", "nepal", "netherlands",
    "new-zealand", "nicaragua", "niger", "nigeria", "north-korea", "norway",
    "oman", "pakistan", "panama", "papua-new-guinea", "paraguay", "peru",
    "philippines", "poland", "portugal", "qatar", "romania", "russia", "rwanda",
    "saudi-arabia", "senegal", "serbia", "sierra-leone", "slovakia", "slovenia",
    "somalia", "south-africa", "south-korea", "spain", "sri-lanka", "sudan",
    "suriname", "swaziland", "sweden", "switzerland", "syria", "taiwan",
    "tajikistan", "tanzania", "thailand", "togo", "tunisia", "turkey",
    "turkmenistan", "uganda", "ukraine", "united-arab-emirates", "united-kingdom",
    "united-states", "uruguay", "uzbekistan", "venezuela", "vietnam", "yemen",
    "zambia", "zimbabwe",
)
_US_STATES = (
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
    "connecticut", "delaware", "florida", "hawaii", "idaho", "illinois",
    "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine", "maryland",
    "massachusetts", "michigan", "minnesota", "mississippi", "missouri",
    "montana", "nebraska", "nevada", "new-hampshire", "new-jersey", "new-mexico",
    "new-york", "north-carolina", "north-dakota", "ohio", "oklahoma", "oregon",
    "pennsylvania", "rhode-island", "south-carolina", "south-dakota", "tennessee",
    "texas", "utah", "vermont", "virginia", "washington", "west-virginia",
    "wisconsin", "wyoming",
)
# (slug, level). "georgia" appears only under country; drop the US-state dup.
REGIONS = (
    tuple((s, "continent") for s in _CONTINENTS)
    + tuple((s, "country") for s in _COUNTRIES)
    + tuple((s, "us-state") for s in _US_STATES if s != "georgia")
)

# --------------------------------------------------------------------------- #
# Schema
# --------------------------------------------------------------------------- #
SCHEMA_TS = pa.schema([
    ("region_slug", pa.string()),
    ("region_name", pa.string()),
    ("level", pa.string()),               # global | continent | country | us-state
    ("variable", pa.string()),            # TAVG | TMAX | TMIN
    ("surface", pa.string()),             # land | land_ocean
    ("year", pa.int16()),
    ("month", pa.int8()),
    ("monthly_anomaly", pa.float64()),
    ("monthly_unc", pa.float64()),
    ("annual_anomaly", pa.float64()),
    ("annual_unc", pa.float64()),
    ("five_year_anomaly", pa.float64()),
    ("five_year_unc", pa.float64()),
    ("ten_year_anomaly", pa.float64()),
    ("ten_year_unc", pa.float64()),
    ("twenty_year_anomaly", pa.float64()),
    ("twenty_year_unc", pa.float64()),
])

# --------------------------------------------------------------------------- #
# Text "Trend" parsing
# --------------------------------------------------------------------------- #
# Data lines: Year, Month, then 5 (anomaly, uncertainty) pairs — monthly, annual,
# five-year, ten-year, twenty-year. 12 whitespace-delimited tokens, "NaN" = missing.
#
# A few files stack TWO data sections under separate commented headers — notably
# Land_and_Ocean_complete.txt, which reports the global series twice (sea ice
# inferred from air temperatures, then from water temperatures). We keep only the
# FIRST section: the air-temperature method is Berkeley Earth's headline series,
# and taking both would produce duplicate (year, month) keys. We detect the second
# section by a commented line reappearing after data has started; for the common
# single-section file the break never fires.
_NCOLS = 12


def _parse_trend(text: str):
    cols = [[] for _ in range(_NCOLS)]
    in_data = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("%"):
            if in_data:
                break  # start of a second series block — keep only the first
            continue
        if not s:
            continue
        parts = s.split()
        if len(parts) != _NCOLS:
            continue
        try:
            year = int(parts[0])
            month = int(parts[1])
        except ValueError:
            continue
        in_data = True
        cols[0].append(year)
        cols[1].append(month)
        for i, tok in enumerate(parts[2:]):
            cols[2 + i].append(None if tok.lower() == "nan" else float(tok))
    return cols


def _region_name(slug: str) -> str:
    return slug.replace("-", " ").title()


def _build_ts_table(meta: dict, cols) -> pa.Table | None:
    n = len(cols[0])
    if n == 0:
        return None
    data = {
        "region_slug": [meta["slug"]] * n,
        "region_name": [meta["name"]] * n,
        "level": [meta["level"]] * n,
        "variable": [meta["variable"]] * n,
        "surface": [meta["surface"]] * n,
        "year": cols[0],
        "month": cols[1],
        "monthly_anomaly": cols[2],
        "monthly_unc": cols[3],
        "annual_anomaly": cols[4],
        "annual_unc": cols[5],
        "five_year_anomaly": cols[6],
        "five_year_unc": cols[7],
        "ten_year_anomaly": cols[8],
        "ten_year_unc": cols[9],
        "twenty_year_anomaly": cols[10],
        "twenty_year_unc": cols[11],
    }
    return pa.table(data, schema=SCHEMA_TS)


# --------------------------------------------------------------------------- #
# Download
# --------------------------------------------------------------------------- #
def fetch_timeseries(node_id: str) -> None:
    """Stateless full re-pull of every global + regional Trend file into one parquet."""
    asset = node_id

    jobs: list[tuple[str, dict]] = []
    for fname, var, surface in GLOBAL_PRODUCTS:
        jobs.append((
            BASE_S3 + "Global/" + fname,
            {"slug": "global", "name": "Global", "level": "global",
             "variable": var, "surface": surface},
        ))
    for slug, level in REGIONS:
        for var in VARIABLES:
            url = f"{BASE_AUTO}Regional/{var}/Text/{slug}-{var}-Trend.txt"
            jobs.append((
                url,
                {"slug": slug, "name": _region_name(slug), "level": level,
                 "variable": var, "surface": "land"},
            ))

    tables: list[pa.Table] = []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(fetch_text, url): meta for url, meta in jobs}
        for fut in cf.as_completed(futures):
            meta = futures[fut]
            text = fut.result()  # transient-exhausted / bug errors propagate
            if text is None:
                continue
            table = _build_ts_table(meta, _parse_trend(text))
            if table is not None:
                tables.append(table)

    if not tables:
        raise RuntimeError("temperature-timeseries: no Trend files fetched")
    save_raw_parquet(pa.concat_tables(tables), asset)


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(
        id="berkeley-earth-temperature-timeseries",
        fn=fetch_timeseries,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="berkeley-earth-temperature-timeseries-transform",
        deps=["berkeley-earth-temperature-timeseries"],
        sql='''
            SELECT
                region_slug,
                region_name,
                level,
                variable,
                surface,
                make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
                CAST(year AS INTEGER)  AS year,
                CAST(month AS INTEGER) AS month,
                monthly_anomaly,
                monthly_unc,
                annual_anomaly,
                annual_unc,
                five_year_anomaly,
                five_year_unc,
                ten_year_anomaly,
                ten_year_unc,
                twenty_year_anomaly,
                twenty_year_unc
            FROM "berkeley-earth-temperature-timeseries"
            WHERE monthly_anomaly IS NOT NULL
        ''',
    ),
]
