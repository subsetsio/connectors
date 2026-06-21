"""IOM connector — two flagship statistical bulk-CSV feeds.

Both subsets are single unauthenticated bulk CSVs re-pulled in full every run
(stateless full re-pull — each file is a few MB / a few hundred k rows, so a
watermark would only risk silently skipping the source's frequent revisions):

  - iom-dtm-displacement : Displacement Tracking Matrix global IDP figures,
        admin levels 0-2. Resolved via the HDX CKAN package record (the
        resource UUID versions, so we never hardcode it).
  - iom-missing-migrants : Missing Migrants Project incident-level records
        (deaths/disappearances along migratory routes, 2014-present), fetched
        directly from missingmigrants.iom.int.

Raw is saved as all-string parquet (faithful copy of the CSV cells, "" -> null);
the TRANSFORM_SPECS SQL is the typing/correctness gate that casts and publishes.

Missing Migrants sits behind a WAF that 403s both our default User-Agent and
browser-like UAs but serves a 200 to a plain bot UA (observed while probing) --
hence the explicit MM_HEADERS below.
"""
import csv
import io

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

# --- sources ----------------------------------------------------------------

HDX_PACKAGE_SHOW = "https://data.humdata.org/api/3/action/package_show"
DTM_HDX_PACKAGE = "global-iom-dtm-from-api"

MM_CSV_URL = (
    "https://missingmigrants.iom.int/sites/g/files/tmzbdl601/files/"
    "report-migrant-incident/Missing_Migrants_Global_Figures_allData.csv"
)
# This host's WAF blocks the default and browser UAs but allows a plain bot UA.
MM_HEADERS = {"User-Agent": "subsets-bot/1.0"}

# CSV header -> snake_case raw column name. Authoritative column contract;
# a missing header raises (the source changed shape) rather than silently
# producing a short table. 'id' is dropped from DTM (always blank upstream).
DTM_COLUMNS = {
    "operation": "operation",
    "admin0Name": "admin0_name",
    "admin0Pcode": "admin0_pcode",
    "admin1Name": "admin1_name",
    "admin1Pcode": "admin1_pcode",
    "admin2Name": "admin2_name",
    "admin2Pcode": "admin2_pcode",
    "adminLevel": "admin_level",
    "numPresentIdpInd": "num_present_idp_ind",
    "reportingDate": "reporting_date",
    "yearReportingDate": "year_reporting_date",
    "monthReportingDate": "month_reporting_date",
    "roundNumber": "round_number",
    "displacementReason": "displacement_reason",
    "numberMales": "number_males",
    "numberFemales": "number_females",
    "idpOriginAdmin1Name": "idp_origin_admin1_name",
    "idpOriginAdmin1Pcode": "idp_origin_admin1_pcode",
    "assessmentType": "assessment_type",
    "operationStatus": "operation_status",
}

MM_COLUMNS = {
    "Main ID": "main_id",
    "Incident ID": "incident_id",
    "Incident Type": "incident_type",
    "Region of Incident": "region_of_incident",
    "Incident Date": "incident_date",
    "Incident Year": "incident_year",
    "Month": "month",
    "Number of Dead": "number_dead",
    "Minimum Estimated Number of Missing": "min_estimated_missing",
    "Total Number of Dead and Missing": "total_dead_and_missing",
    "Number of Survivors": "number_survivors",
    "Number of Females": "number_females",
    "Number of Males": "number_males",
    "Number of Children": "number_children",
    "Country of Origin": "country_of_origin",
    "Region of Origin": "region_of_origin",
    "Cause of Death": "cause_of_death",
    "Country of Incident": "country_of_incident",
    "Migration Route": "migration_route",
    "Location of Incident": "location_of_incident",
    "Coordinates": "coordinates",
    "UNSD Geographical Grouping": "unsd_geographical_grouping",
    "Information Source": "information_source",
    "URL": "source_url",
    "Source Quality": "source_quality",
}


# --- helpers ----------------------------------------------------------------


@transient_retry()
def _http_get(url, *, headers=None, params=None):
    resp = get(url, headers=headers or {}, params=params or {}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp


def _parse_csv(content_bytes):
    """Return (header, rows) from CSV bytes, stripping a UTF-8 BOM if present."""
    text = content_bytes.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    rows = list(reader)
    return header, rows


def _save_csv_as_parquet(header, rows, colmap, asset):
    """Write the selected CSV columns as an all-string parquet ("" -> null)."""
    idx = {h: i for i, h in enumerate(header)}
    missing = [h for h in colmap if h not in idx]
    if missing:
        raise AssertionError(f"{asset}: CSV header missing expected columns: {missing}")

    schema = pa.schema([pa.field(name, pa.string()) for name in colmap.values()])
    columns = {}
    for src_col, name in colmap.items():
        i = idx[src_col]
        columns[name] = [
            (row[i] if i < len(row) and row[i] != "" else None) for row in rows
        ]
    table = pa.Table.from_pydict(columns, schema=schema)
    save_raw_parquet(table, asset)


def _resolve_dtm_csv_url():
    pkg = _http_get(HDX_PACKAGE_SHOW, params={"id": DTM_HDX_PACKAGE}).json()["result"]
    resources = pkg.get("resources", [])
    # Prefer the combined admin 0-2 CSV; fall back to any CSV resource.
    csvs = [r for r in resources if (r.get("format") or "").lower() == "csv"]
    for r in csvs:
        if "admin" in (r.get("name") or "").lower():
            return r["url"]
    if csvs:
        return csvs[0]["url"]
    raise AssertionError("no CSV resource found in HDX package " + DTM_HDX_PACKAGE)


# --- fetch fns --------------------------------------------------------------


def fetch_dtm(node_id):
    asset = node_id
    url = _resolve_dtm_csv_url()
    header, rows = _parse_csv(_http_get(url).content)
    _save_csv_as_parquet(header, rows, DTM_COLUMNS, asset)


def fetch_missing_migrants(node_id):
    asset = node_id
    header, rows = _parse_csv(_http_get(MM_CSV_URL, headers=MM_HEADERS).content)
    _save_csv_as_parquet(header, rows, MM_COLUMNS, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="iom-dtm-displacement", fn=fetch_dtm, kind="download"),
    NodeSpec(id="iom-missing-migrants", fn=fetch_missing_migrants, kind="download"),
]


# --- transforms (one published Delta table per subset) ----------------------

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="iom-dtm-displacement-transform",
        deps=["iom-dtm-displacement"],
        sql='''
            SELECT
                operation,
                admin0_name,
                admin0_pcode,
                admin1_name,
                admin1_pcode,
                admin2_name,
                admin2_pcode,
                TRY_CAST(admin_level AS INTEGER)            AS admin_level,
                TRY_CAST(num_present_idp_ind AS BIGINT)     AS num_present_idp_ind,
                TRY_CAST(substr(reporting_date, 1, 10) AS DATE) AS reporting_date,
                TRY_CAST(year_reporting_date AS INTEGER)    AS year_reporting_date,
                TRY_CAST(month_reporting_date AS INTEGER)   AS month_reporting_date,
                TRY_CAST(round_number AS INTEGER)           AS round_number,
                displacement_reason,
                TRY_CAST(number_males AS BIGINT)            AS number_males,
                TRY_CAST(number_females AS BIGINT)          AS number_females,
                NULLIF(idp_origin_admin1_name, 'Not available')  AS idp_origin_admin1_name,
                NULLIF(idp_origin_admin1_pcode, 'Not available') AS idp_origin_admin1_pcode,
                assessment_type,
                operation_status
            FROM "iom-dtm-displacement"
            WHERE TRY_CAST(num_present_idp_ind AS BIGINT) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iom-missing-migrants-transform",
        deps=["iom-missing-migrants"],
        sql='''
            SELECT
                main_id,
                incident_id,
                incident_type,
                region_of_incident,
                TRY_CAST(incident_date AS DATE)             AS incident_date,
                TRY_CAST(incident_year AS INTEGER)          AS incident_year,
                month,
                TRY_CAST(number_dead AS BIGINT)             AS number_dead,
                TRY_CAST(min_estimated_missing AS BIGINT)   AS min_estimated_missing,
                TRY_CAST(total_dead_and_missing AS BIGINT)  AS total_dead_and_missing,
                TRY_CAST(number_survivors AS BIGINT)        AS number_survivors,
                TRY_CAST(number_females AS BIGINT)          AS number_females,
                TRY_CAST(number_males AS BIGINT)            AS number_males,
                TRY_CAST(number_children AS BIGINT)         AS number_children,
                country_of_origin,
                region_of_origin,
                cause_of_death,
                country_of_incident,
                migration_route,
                location_of_incident,
                coordinates,
                unsd_geographical_grouping,
                information_source,
                source_url,
                TRY_CAST(source_quality AS INTEGER)         AS source_quality
            FROM "iom-missing-migrants"
            WHERE main_id IS NOT NULL
        ''',
    ),
]
