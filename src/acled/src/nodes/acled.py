"""ACLED connector — aggregated conflict time series via the HDX (data.humdata.org) CKAN API.

Access strategy (research-chosen mechanism `ckan_hdx`):
  ACLED publishes weekly-refreshed aggregated XLSX files on the Humanitarian Data
  Exchange. The three global thematic datasets each carry a single XLSX whose
  sheets cover BOTH granularities we publish:
    - `Non_HRP`        : country-month-year counts for the ~219 non-crisis countries.
    - `HRP_1`,`HRP_2`,…: admin1/admin2-month-year counts for the 24 HRP/crisis countries.
  So all six subsets come from just three files — no need to iterate the ~243
  per-country datasets (whose rows are redundant with these global sheets).

  National table  = Non_HRP rows  ∪  HRP rows aggregated up to country-month-year
                    (events/fatalities are additive ACLED counts, so summing the
                    admin2 breakdown reproduces the country total; this is how the
                    24 HRP countries get their country-level series, 1997-present).
  Subnational table = the HRP_* sheets as-is (admin2-month-year, 24 HRP countries).

Download URLs are NOT hardcoded: the resource UUID is stable but the filename
carries an `as-of-<date>` stamp that rotates weekly, so we re-resolve the current
download URL via `package_show` on every run.

Refresh shape: stateless full re-pull. HDX exposes no row-level since/cursor param
(data_update_frequency=7, full XLSX re-published weekly); the files are small
(~40MB) so we re-fetch and overwrite each run, which also picks up revisions for
free. The disaggregated event-level native ACLED API is OAuth-gated and out of
scope for this servable path.
"""
import io

import httpx
import pandas as pd
import pyarrow as pa
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import NodeSpec, SqlNodeSpec, get, is_transient, save_raw_parquet

CKAN = "https://data.humdata.org/api/3/action/"

# HDX sits behind Cloudflare bot management: requests from datacenter IPs with a
# non-browser User-Agent get a 202 + empty body (a silent soft-block) instead of
# the JSON. A realistic browser UA clears the challenge; Accept pins JSON.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, */*",
}

# entity_id -> (HDX package/dataset name, scope, has_fatalities). Each download
# spec id is f"acled-{entity_id}"; the entity ids are the rank-accepted union.
CONFIG = {
    "political-violence-events-and-fatalities": ("political-violence-events-and-fatalities", "national",    True),
    "political-violence-subnational":           ("political-violence-events-and-fatalities", "subnational", True),
    "civilian-targeting-events-and-fatalities": ("civilian-targeting-events-and-fatalities", "national",    True),
    "civilian-targeting-subnational":           ("civilian-targeting-events-and-fatalities", "subnational", True),
    "demonstration-events":                     ("demonstration-events",                     "national",    False),
    "demonstration-events-subnational":         ("demonstration-events",                     "subnational", False),
}

ENTITY_IDS = list(CONFIG)

# Source XLSX headers -> our snake_case raw columns.
_RENAME = {
    "Country": "country", "Admin1": "admin1", "Admin2": "admin2", "ISO3": "iso3",
    "Admin1 Pcode": "admin1_pcode", "Admin2 Pcode": "admin2_pcode",
    "Month": "month", "Year": "year", "Events": "events", "Fatalities": "fatalities",
}

# ---------------------------------------------------------------------------
# HTTP with honest retry semantics
# ---------------------------------------------------------------------------
class _Challenged(Exception):
    """Raised when HDX/Cloudflare returns a non-200 'accepted'/challenge response
    (e.g. 202 + empty body) instead of the payload. Always retried."""


def _is_transient(exc: BaseException) -> bool:
    # standard transient policy, plus acled's Cloudflare challenge response
    return is_transient(exc) or isinstance(exc, _Challenged)


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_json(url: str, **params) -> dict:
    resp = get(url, params=params, headers=_HEADERS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    if resp.status_code != 200:
        raise _Challenged(f"{url}: expected 200, got {resp.status_code} "
                          f"({len(resp.content)} bytes)")
    try:
        return resp.json()
    except ValueError as e:
        raise _Challenged(f"{url}: non-JSON body ({len(resp.content)} bytes)") from e


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_bytes(url: str) -> bytes:
    resp = get(url, headers=_HEADERS, timeout=(10.0, 300.0))
    resp.raise_for_status()
    if resp.status_code != 200:
        raise _Challenged(f"{url}: expected 200, got {resp.status_code} "
                          f"({len(resp.content)} bytes)")
    return resp.content


def _resolve_xlsx_url(pkg: str) -> str:
    """Re-resolve the current XLSX download URL for a dataset (the filename carries
    a weekly as-of stamp, so we never hardcode it)."""
    result = _get_json(CKAN + "package_show", id=pkg)["result"]
    xlsx = [r for r in result["resources"] if (r.get("format") or "").upper() == "XLSX"]
    if not xlsx:
        raise AssertionError(f"{pkg}: no XLSX resource found on HDX")
    return xlsx[0]["url"]


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def _national_schema(has_fat: bool) -> pa.Schema:
    fields = [("country", pa.string()), ("month", pa.string()),
              ("year", pa.int64()), ("events", pa.int64())]
    if has_fat:
        fields.append(("fatalities", pa.int64()))
    return pa.schema(fields)


def _subnational_schema(has_fat: bool) -> pa.Schema:
    fields = [("country", pa.string()), ("admin1", pa.string()), ("admin2", pa.string()),
              ("iso3", pa.string()), ("admin1_pcode", pa.string()),
              ("admin2_pcode", pa.string()), ("month", pa.string()),
              ("year", pa.int64()), ("events", pa.int64())]
    if has_fat:
        fields.append(("fatalities", pa.int64()))
    return pa.schema(fields)


def _coerce(df: pd.DataFrame, schema: pa.Schema) -> pa.Table:
    df = df[list(schema.names)].copy()
    df["year"] = df["year"].astype("int64")
    for c in ("events", "fatalities"):
        if c in df.columns:
            df[c] = df[c].fillna(0).astype("int64")
    return pa.Table.from_pandas(df, schema=schema, preserve_index=False)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("acled-"):]
    pkg, scope, has_fat = CONFIG[entity_id]

    url = _resolve_xlsx_url(pkg)
    xls = pd.ExcelFile(io.BytesIO(_get_bytes(url)))
    sheets = xls.sheet_names
    hrp_sheets = [s for s in sheets if s.upper().startswith("HRP_")]
    non_hrp_sheets = [s for s in sheets if s.lower() == "non_hrp"]

    sub = pd.concat([pd.read_excel(xls, sheet_name=s) for s in hrp_sheets],
                    ignore_index=True).rename(columns=_RENAME)

    if scope == "subnational":
        table = _coerce(sub, _subnational_schema(has_fat))
    else:  # national: Non_HRP rows + HRP aggregated to country-month-year
        agg_cols = ["events"] + (["fatalities"] if has_fat else [])
        keys = ["country", "month", "year"]
        nat_hrp = sub.groupby(keys, as_index=False)[agg_cols].sum()
        nat_non = pd.concat(
            [pd.read_excel(xls, sheet_name=s) for s in non_hrp_sheets],
            ignore_index=True).rename(columns=_RENAME)
        nat = pd.concat([nat_non[keys + agg_cols], nat_hrp[keys + agg_cols]],
                        ignore_index=True)
        table = _coerce(nat, _national_schema(has_fat))

    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"acled-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# ---------------------------------------------------------------------------
# Transforms — one published Delta table per subset. Thin: parse month name +
# year into a first-of-month DATE, cast counts, project. No dedup needed (rows
# are unique per country[-admin2]-month-year).
# ---------------------------------------------------------------------------
_DATE = "CAST(strptime(month || ' ' || CAST(year AS VARCHAR), '%B %Y') AS DATE) AS date"


def _transform_sql(download_id: str, scope: str, has_fat: bool) -> str:
    fat = ",\n            CAST(fatalities AS BIGINT) AS fatalities" if has_fat else ""
    if scope == "subnational":
        return f'''
        SELECT
            {_DATE},
            country, admin1, admin2, iso3, admin1_pcode, admin2_pcode,
            CAST(events AS BIGINT) AS events{fat}
        FROM "{download_id}"
        WHERE month IS NOT NULL AND year IS NOT NULL
        '''
    return f'''
        SELECT
            {_DATE},
            country,
            CAST(events AS BIGINT) AS events{fat}
        FROM "{download_id}"
        WHERE month IS NOT NULL AND year IS NOT NULL
        '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"acled-{eid}-transform",
        deps=[f"acled-{eid}"],
        sql=_transform_sql(f"acled-{eid}", scope, has_fat),
    )
    for eid, (_pkg, scope, has_fat) in CONFIG.items()
]
