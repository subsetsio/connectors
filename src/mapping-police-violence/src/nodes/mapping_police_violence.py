"""Mapping Police Violence — the full police-killings database (one row per person
killed by police in the US since 2013, ~15.9k rows, 62 columns).

Source: a public Airtable shared grid view (base appzVzSeINK1S3EVR, share
shroOenW19l1m3w0H, view viwFu0gBYA38MT2A8) — the dataset behind the
mappingpoliceviolence.org "Download the Data" button. One unauthenticated GET to
readSharedViewData returns the entire corpus in one JSON response. The request
needs a short-lived signed accessPolicy that Airtable embeds, fresh, in the
shared-view HTML page as a ready-built `urlWithParams` field; we scrape it each
run rather than hardcoding it (the signature expires ~monthly).
"""

import re

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry

SHARE_PAGE = "https://airtable.com/appzVzSeINK1S3EVR/shroOenW19l1m3w0H/tblxearKzw8W7ViN8"
_HOST = "https://airtable.com"
_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
_API_HEADERS = {
    "User-Agent": _UA,
    "x-airtable-application-id": "appzVzSeINK1S3EVR",
    "x-airtable-inter-service-client": "webClient",
    "x-requested-with": "XMLHttpRequest",
    # Airtable 400s with BAD_REQUEST if these two are absent.
    "x-time-zone": "America/New_York",
    "x-user-locale": "en",
    "Accept": "application/json",
}


@transient_retry()
def _get_view_data() -> dict:
    # 1) scrape the shared-view page for a freshly-signed readSharedViewData url.
    html = get(SHARE_PAGE, headers={"User-Agent": _UA}, timeout=60).text
    m = re.search(r'urlWithParams:\s*"([^"]+)"', html)
    if not m:
        raise RuntimeError(
            "Airtable share page no longer exposes urlWithParams — shared-view "
            "format changed; the readSharedViewData signing flow needs revisiting."
        )
    url = _HOST + m.group(1).encode().decode("unicode_escape")

    # 2) one request returns the whole corpus (no pagination).
    resp = get(url, headers=_API_HEADERS, timeout=180)
    resp.raise_for_status()
    data = resp.json()
    if "data" not in data or "table" not in data["data"]:
        raise RuntimeError(f"unexpected readSharedViewData response keys: {list(data)}")
    return data["data"]["table"]


def _flatten_rows(table: dict) -> list[dict]:
    columns = table["columns"]
    # column id -> display name
    col_name = {c["id"]: c["name"] for c in columns}
    # for select/multiSelect columns, choice id -> human label
    choice_maps: dict[str, dict] = {}
    for c in columns:
        if c["type"] in ("select", "multiSelect"):
            choices = (c.get("typeOptions") or {}).get("choices") or {}
            choice_maps[c["id"]] = {cid: ch.get("name") for cid, ch in choices.items()}

    out: list[dict] = []
    for row in table["rows"]:
        flat: dict = {name: None for name in col_name.values()}
        for cid, val in row["cellValuesByColumnId"].items():
            name = col_name.get(cid)
            if name is None:
                continue
            cmap = choice_maps.get(cid)
            if cmap is not None:
                if isinstance(val, list):
                    # multiSelect — list of choice ids -> "; "-joined labels
                    val = "; ".join(str(cmap.get(v, v)) for v in val) or None
                elif isinstance(val, str):
                    val = cmap.get(val, val)
            elif name == "date" and isinstance(val, str) and len(val) >= 10:
                # ISO timestamp at UTC midnight -> calendar date
                val = val[:10]
            flat[name] = val
        out.append(flat)
    return out


def fetch_killings(node_id: str) -> None:
    table = _get_view_data()
    rows = _flatten_rows(table)
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="mapping-police-violence-mapping-police-violence-killings", fn=fetch_killings, kind="download"),
]


_SQL_KILLINGS = """
SELECT
    name,
    TRY_CAST(age AS INTEGER)                              AS age,
    gender,
    race,
    CAST(date AS DATE)                                    AS date,
    street_address,
    city,
    state,
    zip,
    county,
    agency_responsible,
    ori,
    cause_of_death,
    circumstances,
    disposition_official,
    officer_charged,
    signs_of_mental_illness,
    allegedly_armed,
    wapo_armed,
    wapo_threat_level,
    wapo_flee,
    wapo_body_camera,
    TRY_CAST(wapo_id AS BIGINT)                           AS wapo_id,
    off_duty_killing,
    geography,
    TRY_CAST(mpv_id AS BIGINT)                            AS mpv_id,
    TRY_CAST(fe_id AS BIGINT)                             AS fe_id,
    encounter_type,
    initial_reason,
    officer_names,
    officer_races,
    officer_known_past_shootings,
    call_for_service,
    TRY_CAST(tract AS BIGINT)                             AS tract,
    urban_rural_uspsai,
    urban_rural_nchs,
    TRY_CAST(hhincome_median_census_tract AS BIGINT)     AS hhincome_median_census_tract,
    TRY_CAST(latitude AS DOUBLE)                          AS latitude,
    TRY_CAST(longitude AS DOUBLE)                         AS longitude,
    TRY_CAST(pop_total_census_tract AS BIGINT)           AS pop_total_census_tract,
    TRY_CAST(pop_white_census_tract AS DOUBLE)           AS pop_white_census_tract,
    TRY_CAST(pop_black_census_tract AS DOUBLE)           AS pop_black_census_tract,
    TRY_CAST(pop_native_american_census_tract AS DOUBLE) AS pop_native_american_census_tract,
    TRY_CAST(pop_asian_census_tract AS DOUBLE)           AS pop_asian_census_tract,
    TRY_CAST(pop_pacific_islander_census_tract AS DOUBLE) AS pop_pacific_islander_census_tract,
    TRY_CAST(pop_other_multiple_census_tract AS DOUBLE)  AS pop_other_multiple_census_tract,
    TRY_CAST(pop_hispanic_census_tract AS DOUBLE)        AS pop_hispanic_census_tract,
    congressional_district_113,
    congressperson_lastname,
    congressperson_firstname,
    congressperson_party,
    prosecutor_head,
    prosecutor_race,
    prosecutor_gender,
    prosecutor_party,
    prosecutor_term,
    prosecutor_in_court,
    prosecutor_special,
    independent_investigation,
    prosecutor_url
FROM "mapping-police-violence-mapping-police-violence-killings"
WHERE mpv_id IS NOT NULL
"""

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="mapping-police-violence-killings-transform",
        deps=["mapping-police-violence-mapping-police-violence-killings"],
        sql=_SQL_KILLINGS,
    ),
]
