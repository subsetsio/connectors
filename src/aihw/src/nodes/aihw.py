"""AIHW (Australian Institute of Health and Welfare) connector.

Two fetch paths, both stateless full re-pulls (the whole corpus re-fetched each
run and overwritten — every source here is small enough and exposes no delta
filter, per research):

  * 9 CKAN CSV products on data.gov.au (national mortality/cancer/expenditure/
    survey statistics). Resource download URLs are resolved at fetch time via
    the CKAN `resource_show` action (AIHW re-versions filenames on refresh).
    Each CSV is decoded (UTF-8 with a cp1252 fallback — MORT files are cp1252),
    parsed, and saved as NDJSON of string cells; the transform casts.
  * `reporting_units` — the MyHospitals reporting-unit directory (one reliable
    JSON call). MyHospitals content-negotiates: it returns CSV unless you send
    `Accept: application/json`, and prefixes JSON with a UTF-8 BOM.

Each download has exactly one SQL transform that casts/cleans and publishes one
Delta table.
"""

import csv
import io
import json

import pyarrow as pa  # noqa: F401  (kept available; not needed for NDJSON path)
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

from constants import CKAN_RESOURCE_IDS

CKAN_ACTION = "https://data.gov.au/data/api/3/action"
MYH_BASE = "https://myhospitalsapi.aihw.gov.au/api/v1"
JSON_HEADERS = {"Accept": "application/json"}


# --------------------------------------------------------------------------- #
# fetch helpers
# --------------------------------------------------------------------------- #
def _spec_to_resource_id(node_id: str) -> str:
    """`aihw-<uuid>` -> `<uuid>` (CKAN resource ids are already lowercase hyphenated)."""
    return node_id[len("aihw-"):]


def _decode_csv_bytes(raw: bytes) -> str:
    """AIHW CSVs are mostly UTF-8 (BOM) but the MORT books are cp1252. Try the
    strict UTF-8 path first; fall back to cp1252 so the en-dashes in year ranges
    and ICD code ranges survive."""
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1252")


@transient_retry()
def _ckan_resource_url(resource_id: str) -> str:
    resp = get(
        f"{CKAN_ACTION}/resource_show",
        params={"id": resource_id},
        timeout=(10.0, 60.0),
    )
    resp.raise_for_status()
    return resp.json()["result"]["url"]


@transient_retry()
def _download_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_ckan_resource(node_id: str) -> None:
    """Resolve the CKAN resource's download URL, pull the CSV, and persist it as
    NDJSON (one object per row, all cells as strings). The transform owns typing."""
    resource_id = _spec_to_resource_id(node_id)
    url = _ckan_resource_url(resource_id)
    text = _decode_csv_bytes(_download_bytes(url))
    reader = csv.DictReader(io.StringIO(text))
    # DictReader streams rows lazily; save_raw_ndjson consumes the iterator.
    save_raw_ndjson(reader, node_id)


@transient_retry()
def _myh_json(path: str):
    resp = get(f"{MYH_BASE}/{path}", headers=JSON_HEADERS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return json.loads(resp.content.decode("utf-8-sig"))


def fetch_reporting_units(node_id: str) -> None:
    """The MyHospitals reporting-unit directory: hospitals, local hospital
    networks, peer groups and states with codes, names, types and lat/long.
    Flattened to scalar columns (the nested mapping/meta-tag arrays are dropped)."""
    units = _myh_json("reporting-units")["result"]
    rows = []
    for u in units:
        rut = u.get("reporting_unit_type") or {}
        rows.append(
            {
                "reporting_unit_code": u.get("reporting_unit_code"),
                "reporting_unit_name": u.get("reporting_unit_name"),
                "reporting_unit_type_code": rut.get("reporting_unit_type_code"),
                "reporting_unit_type_name": rut.get("reporting_unit_type_name"),
                "latitude": u.get("latitude"),
                "longitude": u.get("longitude"),
                "closed": u.get("closed"),
                "private": u.get("private"),
            }
        )
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# download specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id=f"aihw-{rid}", fn=fetch_ckan_resource, kind="download")
    for rid in CKAN_RESOURCE_IDS
] + [
    NodeSpec(id="aihw-reporting-units", fn=fetch_reporting_units, kind="download"),
]


# --------------------------------------------------------------------------- #
# transform SQL — one published Delta table per download
# --------------------------------------------------------------------------- #
# A column spec is (source_name, output_name, kind) where kind is:
#   "s" string, "i" integer, "d" double.
# Numeric casts strip thousands separators and treat '' as NULL (TRY_CAST keeps
# unparseable cells NULL rather than failing the node).
def _expr(src: str, kind: str) -> str:
    q = f'"{src}"'
    if kind == "s":
        return f"NULLIF(CAST({q} AS VARCHAR), '')"
    cast_to = "BIGINT" if kind == "i" else "DOUBLE"
    cleaned = f"NULLIF(REPLACE(CAST({q} AS VARCHAR), ',', ''), '')"
    return f"TRY_CAST({cleaned} AS {cast_to})"


def _select(view: str, cols, guard_out: str) -> str:
    projection = ",\n        ".join(
        f"{_expr(src, kind)} AS {out}" for src, out, kind in cols
    )
    return (
        f'SELECT * FROM (\n      SELECT\n        {projection}\n      '
        f'FROM "{view}"\n    ) t\n    WHERE {guard_out} IS NOT NULL'
    )


# Shared ACIM age-band columns (20 bands, all rates/counts -> double).
_ACIM_AGE = [
    "Age_0_to_4", "Age_5_to_9", "Age_10_to_14", "Age_15_to_19", "Age_20_to_24",
    "Age_25_to_29", "Age_30_to_34", "Age_35_to_39", "Age_40_to_44", "Age_45_to_49",
    "Age_50_to_54", "Age_55_to_59", "Age_60_to_64", "Age_65_to_69", "Age_70_to_74",
    "Age_75_to_79", "Age_80_to_84", "Age_85+", "Age_Unknown",
]


def _acim_age_cols():
    return [(c, c.lower().replace("+", "_plus"), "d") for c in _ACIM_AGE]


# download_id (without slug munging) -> column spec + guard column.
_CONFIG = {
    # GRIM — national deaths by cause/age/sex/year (1907–2023).
    "edcbc14c-ba7c-44ae-9d4f-2622ad3fafe0": (
        [
            ("grim", "grim_code", "s"),
            ("cause_of_death", "cause_of_death", "s"),
            ("year", "year", "i"),
            ("sex", "sex", "s"),
            ("age_group", "age_group", "s"),
            ("deaths", "deaths", "i"),
            ("crude_rate_per_100000", "crude_rate_per_100000", "d"),
            ("age_standardised_rate_per_100000", "age_standardised_rate_per_100000", "d"),
        ],
        "year",
    ),
    # ACIM Combined Rates — incidence/mortality rates by sex/year/age/cancer.
    "7e4d5726-8daa-4c14-8a46-96b701e8b3ca": (
        [
            ("Year", "year", "i"),
            ("Sex", "sex", "s"),
            ("Type", "type", "s"),
            ("Cancer_Type", "cancer_type", "s"),
        ]
        + _acim_age_cols()
        + [
            ("Age_Std_Rate_Aust", "age_std_rate_aust", "d"),
            ("Age_Std_Rate_Segi", "age_std_rate_segi", "d"),
            ("Age_Std_Rate_WHO", "age_std_rate_who", "d"),
        ],
        "year",
    ),
    # ACIM Combined Counts — incidence/mortality counts (no std-rate columns).
    "7fbac314-4bf9-4601-b812-0307316ef5a4": (
        [
            ("Year", "year", "i"),
            ("Sex", "sex", "s"),
            ("Type", "type", "s"),
            ("Cancer_Type", "cancer_type", "s"),
        ]
        + _acim_age_cols(),
        "year",
    ),
    # ACIM Combined Ratio — mortality-to-incidence ratios.
    "c39b4db3-5d92-4cc1-b49d-92e63fc72b77": (
        [
            ("Year", "year", "i"),
            ("Sex", "sex", "s"),
            ("Cancer_Type", "cancer_type", "s"),
            ("Aust_Mortality_to_incidence_ratio", "aust_mortality_to_incidence_ratio", "d"),
            ("Segi_Mortality_to_incidence_ratio", "segi_mortality_to_incidence_ratio", "d"),
            ("WHO_Mortality_to_incidence_ratio", "who_mortality_to_incidence_ratio", "d"),
        ],
        "year",
    ),
    # MORT_TABLE_2 — leading causes of death by region (year is a period range).
    "3b7d81af-943f-447d-9d64-9ce220be35e7": (
        [
            ("mort", "mort_code", "s"),
            ("category", "category", "s"),
            ("geography", "geography", "s"),
            ("year", "period", "s"),
            ("SEX", "sex", "s"),
            ("rank", "rank", "i"),
            ("cause_of_death", "cause_of_death", "s"),
            ("deaths", "deaths", "i"),
            ("deaths_percent", "deaths_percent", "d"),
            ("crude_rate_per_100000", "crude_rate_per_100000", "d"),
            ("age_standardised_rate_per_100000", "age_standardised_rate_per_100000", "d"),
            ("rate_ratio", "rate_ratio", "d"),
        ],
        "geography",
    ),
    # MORT_TABLE_1 — summary mortality measures by region (year is a period range).
    "a5de4e7e-d062-4356-9d1b-39f44b1961dc": (
        [
            ("mort", "mort_code", "s"),
            ("category", "category", "s"),
            ("geography", "geography", "s"),
            ("YEAR", "period", "s"),
            ("SEX", "sex", "s"),
            ("deaths", "deaths", "i"),
            ("population", "population", "i"),
            ("crude_rate_per_100000", "crude_rate_per_100000", "d"),
            ("age_standardised_rate_per_100000", "age_standardised_rate_per_100000", "d"),
            ("rate_ratio", "rate_ratio", "d"),
            ("premature_deaths", "premature_deaths", "i"),
            ("premature_deaths_percent", "premature_deaths_percent", "d"),
            ("premature_deaths_asr_per_100000", "premature_deaths_asr_per_100000", "d"),
            ("potential_years_of_life_lost", "potential_years_of_life_lost", "i"),
            ("pyll_rate_per_1000", "pyll_rate_per_1000", "d"),
            ("potentially_avoidable_deaths", "potentially_avoidable_deaths", "i"),
            ("pad_percent", "pad_percent", "d"),
            ("pad_asr_per_100000", "pad_asr_per_100000", "d"),
            ("median_age", "median_age", "d"),
        ],
        "geography",
    ),
    # Health expenditure by area and source (constant prices).
    "88399d53-d55c-466c-8f4a-6cb965d24d6d": (
        [
            ("financial_year", "financial_year", "s"),
            ("state", "state", "s"),
            ("area_of_expenditure", "area_of_expenditure", "s"),
            ("broad_source_of_funding", "broad_source_of_funding", "s"),
            ("detailed_source_of_funding", "detailed_source_of_funding", "s"),
            ("real_expenditure_millions", "real_expenditure_millions", "d"),
        ],
        "financial_year",
    ),
    # Youth justice detention — average nightly population, quarterly 2008–2016.
    "c7edfa08-7bc9-404d-8f2b-22bcd0425021": (
        [
            ("agegrp", "age_group", "s"),
            ("indig_status", "indigenous_status", "s"),
            ("legal_status", "legal_status", "s"),
            ("sex", "sex", "s"),
            ("state", "state", "s"),
            ("quarter", "quarter", "s"),
            ("quart", "quarter_short", "s"),
            ("year", "year", "i"),
            ("avg_nightly_pop", "avg_nightly_pop", "d"),
        ],
        "year",
    ),
    # National Drug Strategy Household Survey — respondent-level microdata (codes).
    "5c536ecc-316a-4206-9984-bd1b3b8982b9": (
        [
            ("Weight7", "weight", "d"),
            ("Sex", "sex", "s"),
            ("A1", "a1", "s"),
            ("A2", "a2", "s"),
            ("A3", "a3", "s"),
            ("A4_01", "a4_01", "s"),
            ("A4_02", "a4_02", "s"),
            ("A4_08", "a4_08", "s"),
            ("B1", "b1", "s"),
            ("tobsum", "tobsum", "s"),
            ("AlcSum", "alcsum", "s"),
            ("AgeGroup1460p", "age_group_14_60plus", "s"),
            ("AverageG1", "average_g1", "d"),
            ("G2_week", "g2_week", "s"),
            ("G2_month", "g2_month", "s"),
            ("G2_year", "g2_year", "s"),
            ("Marijuana", "marijuana", "s"),
            ("Anyillicit", "any_illicit", "s"),
            ("Remoteness", "remoteness", "s"),
            ("Age1265", "age_12_65", "s"),
        ],
        "weight",
    ),
}


# Per-resource grain declarations (output-column names). None key = undeclared
# (grain ambiguous); () = genuinely keyless observation microdata.
_GRAIN = {
    # GRIM — national deaths by cause/age/sex/year.
    "edcbc14c-ba7c-44ae-9d4f-2622ad3fafe0": (
        ("grim_code", "year", "sex", "age_group"), "year",
    ),
    # ACIM Combined Rates.
    "7e4d5726-8daa-4c14-8a46-96b701e8b3ca": (
        ("year", "sex", "type", "cancer_type"), "year",
    ),
    # ACIM Combined Counts.
    "7fbac314-4bf9-4601-b812-0307316ef5a4": (
        ("year", "sex", "type", "cancer_type"), "year",
    ),
    # ACIM Combined Ratio.
    "c39b4db3-5d92-4cc1-b49d-92e63fc72b77": (
        ("year", "sex", "cancer_type"), "year",
    ),
    # MORT_TABLE_2 — leading causes by region; ranked-row grain ambiguous.
    "3b7d81af-943f-447d-9d64-9ce220be35e7": (None, "period"),
    # MORT_TABLE_1 — summary measures by region; row-id grain ambiguous.
    "a5de4e7e-d062-4356-9d1b-39f44b1961dc": (None, "period"),
    # Health expenditure by area and source.
    "88399d53-d55c-466c-8f4a-6cb965d24d6d": (
        ("financial_year", "state", "area_of_expenditure",
         "broad_source_of_funding", "detailed_source_of_funding"),
        "financial_year",
    ),
    # Youth justice detention — average nightly population, quarterly.
    "c7edfa08-7bc9-404d-8f2b-22bcd0425021": (
        ("age_group", "indigenous_status", "legal_status", "sex", "state",
         "quarter", "year"),
        "year",
    ),
    # NDSHS — respondent-level survey microdata (no id column): keyless.
    "5c536ecc-316a-4206-9984-bd1b3b8982b9": ((), None),
}


def _ckan_transforms():
    specs = []
    for rid, (cols, guard) in _CONFIG.items():
        download_id = f"aihw-{rid}"
        guard_out = next(out for _, out, _ in cols if out == guard)
        key, temporal = _GRAIN.get(rid, (None, None))
        specs.append(
            SqlNodeSpec(
                id=f"{download_id}-transform",
                deps=[download_id],
                sql=_select(download_id, cols, guard_out),
                key=key,
                temporal=temporal,
            )
        )
    return specs


_REPORTING_UNITS_SQL = """
    SELECT
        reporting_unit_code,
        reporting_unit_name,
        reporting_unit_type_code,
        reporting_unit_type_name,
        TRY_CAST(latitude AS DOUBLE)  AS latitude,
        TRY_CAST(longitude AS DOUBLE) AS longitude,
        CAST(closed AS BOOLEAN)       AS closed,
        CAST(private AS BOOLEAN)      AS private
    FROM "aihw-reporting-units"
    WHERE reporting_unit_code IS NOT NULL
"""

TRANSFORM_SPECS = _ckan_transforms() + [
    SqlNodeSpec(
        id="aihw-reporting-units-transform",
        deps=["aihw-reporting-units"],
        sql=_REPORTING_UNITS_SQL,
        key=("reporting_unit_code",),
    ),
]
