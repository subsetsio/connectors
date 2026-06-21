"""National Interagency Fire Center (NIFC) connector.

NIFC publishes its authoritative interagency wildland-fire data through ArcGIS
feature services hosted in its ArcGIS Online org (org id T4QMspbfLg3qTGWY;
VIIRS hotspots live in a separate Esri Living-Atlas org). Each published subset
is one ArcGIS FeatureServer/Table layer with its own column schema.

Mechanism (from research): `arcgis_rest`. Each layer is queried at
`<service>/<layer>/query` with `where=1=1, outFields=*, returnGeometry=false,
f=json`, paginated by `resultOffset` in steps of `resultRecordCount` until the
server stops setting `exceededTransferLimit`. No auth, no documented rate limit.

Fetch shape: stateless full re-pull (shape 1). Every refresh re-pulls each
layer in full and overwrites — the layers are at most ~1.2M rows and re-pulling
is cheap relative to maintaining a watermark, and it picks up upstream revisions
for free. Raw is streamed to gzip-compressed NDJSON (records are wide — 16-120
attributes, many sparse — so NDJSON beats a fixed parquet schema), keeping
memory flat on the large layers. ArcGIS date fields arrive as epoch-millisecond
integers and are converted with DuckDB `epoch_ms()` in the transforms.
"""
import json


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    transient_retry,
)

SLUG = "nifc"
PREFIX = f"{SLUG}-"

# Each entity id (from the rank-accepted entity union) maps to its live ArcGIS
# layer query base and a per-layer page size (VIIRS allows a far larger page).
_S3 = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services"
LAYERS = {
    "29185087b4594a35abe059cbdbf97ee4-1": {  # RAWS weather stations (current obs)
        "url": f"{_S3}/PublicView_RAWS/FeatureServer/1", "page": 2000},
    "5e72b1699bf74eefb3f3aff6f4ba5511-0": {  # WFIGS Interagency Fire Perimeters
        "url": f"{_S3}/WFIGS_Interagency_Perimeters/FeatureServer/0", "page": 2000},
    "60a94840152b4a89bec467a9f052f135-0": {  # InFORM Fire Occurrence Data Records
        "url": f"{_S3}/InFORM_FireOccurrence_Public/FeatureServer/0", "page": 2000},
    "b4402f7887ca4ea9a6189443f220ef28-0": {  # Wildland Fire Incident Locations
        "url": f"{_S3}/WFIGS_Incident_Locations/FeatureServer/0", "page": 2000},
    "dece90af1a0242dcbf0ca36d30276aa3-0": {  # VIIRS Thermal Hotspots
        "url": "https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/"
               "Satellite_VIIRS_Thermal_Hotspots_and_Fire_Activity/FeatureServer/0",
        "page": 16000},
    "e02b85c0ea784ce7bd8add7ae3d293d0-0": {  # Interagency Fire Perimeter History (all years)
        "url": f"{_S3}/InterAgencyFirePerimeterHistory_All_Years_View/FeatureServer/0", "page": 2000},
    "eaa333df1850483abdd0465f86212e03-0": {  # IMSR Incident Locations (historical)
        "url": f"{_S3}/IMSR_Incident_Locations_View_Final_Occurrence_Historical/FeatureServer/0", "page": 2000},
    "ef25d7e8c9f3499ba9e3d8e09606e488-0": {  # Historic GeoMAC Perimeters Combined 2000-2018
        "url": f"{_S3}/Historic_Geomac_Perimeters_Combined_2000_2018/FeatureServer/0", "page": 2000},
}

# Safety ceiling: largest layer is ~1.2M rows -> ~611 pages at 2000/page. This
# cap only fires if the source grows far beyond expectation — it raises (never
# silently truncates) so unexpected growth is surfaced, not hidden.
MAX_PAGES = 5000


@transient_retry()
def _query(layer_url: str, page: int, offset: int) -> dict:
    resp = get(
        f"{layer_url}/query",
        params={
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "false",
            "orderByFields": "OBJECTID",
            "resultRecordCount": page,
            "resultOffset": offset,
            "f": "json",
        },
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    """Re-pull one ArcGIS layer in full and stream its attributes to NDJSON."""
    eid = node_id[len(PREFIX):]
    layer = LAYERS[eid]
    url, page = layer["url"], layer["page"]

    offset = 0
    pages = 0
    total = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as out:
        while True:
            if pages >= MAX_PAGES:
                raise RuntimeError(
                    f"{node_id}: hit MAX_PAGES={MAX_PAGES} at offset {offset} — "
                    "source larger than expected; raise the cap intentionally"
                )
            data = _query(url, page, offset)
            if isinstance(data, dict) and "error" in data:
                raise RuntimeError(f"{node_id}: ArcGIS query error {data['error']}")
            feats = data.get("features", [])
            if not feats:
                break
            for f in feats:
                attrs = f.get("attributes")
                if attrs:
                    out.write(json.dumps(attrs, separators=(",", ":")) + "\n")
                    total += 1
            pages += 1
            offset += len(feats)
            # exceededTransferLimit drops once the final page is served.
            if not data.get("exceededTransferLimit"):
                break
    print(f"  {node_id}: wrote {total:,} records over {pages} page(s)")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid}", fn=fetch_one, kind="download")
    for eid in LAYERS
]


# --- Transforms: one curated, typed Delta table per subset -------------------
# Each SQL projects a clean, well-named column set and converts epoch-ms date
# fields to timestamps via epoch_ms(). DuckDB identifier matching is
# case-insensitive, so the mixed-case ArcGIS attribute keys bind directly.


def _ts(col: str) -> str:
    """Epoch-ms -> TIMESTAMP, NULLing implausible values. NIFC source data
    carries sentinel dates (1899-12-30 = ArcGIS 'no date') and sporadic
    far-future typos (years 2102/2424/3013/6202); bound to a sane window so a
    single bad row can't pollute the published series' freshness."""
    e = f"epoch_ms(TRY_CAST({col} AS BIGINT))"
    return (f"CASE WHEN {e} BETWEEN TIMESTAMP '1900-01-01' "
            f"AND TIMESTAMP '2027-12-31' THEN {e} END")

_RAWS = "nifc-29185087b4594a35abe059cbdbf97ee4-1"
_PERIM = "nifc-5e72b1699bf74eefb3f3aff6f4ba5511-0"
_INFORM = "nifc-60a94840152b4a89bec467a9f052f135-0"
_INCIDENTS = "nifc-b4402f7887ca4ea9a6189443f220ef28-0"
_VIIRS = "nifc-dece90af1a0242dcbf0ca36d30276aa3-0"
_HISTORY = "nifc-e02b85c0ea784ce7bd8add7ae3d293d0-0"
_IMSR = "nifc-eaa333df1850483abdd0465f86212e03-0"
_GEOMAC = "nifc-ef25d7e8c9f3499ba9e3d8e09606e488-0"

_SQL = {
    _RAWS: f'''
        SELECT
            StationID                                AS station_id,
            WXID                                     AS wx_id,
            StationName                              AS station_name,
            NESSID                                   AS ness_id,
            NWSID                                    AS nws_id,
            TRY_CAST(Elevation AS INTEGER)           AS elevation_ft,
            TRY_CAST(Latitude AS DOUBLE)             AS latitude,
            TRY_CAST(Longitude AS DOUBLE)            AS longitude,
            State                                    AS state,
            County                                   AS county,
            Agency                                   AS agency,
            Region                                   AS region,
            Unit                                     AS unit,
            SubUnit                                  AS subunit,
            Status                                   AS status,
            {_ts('ObservedDate')}                    AS observed_at
        FROM "{_RAWS}"
    ''',
    _PERIM: f'''
        SELECT
            attr_UniqueFireIdentifier                AS unique_fire_id,
            COALESCE(attr_IncidentName, poly_IncidentName) AS incident_name,
            attr_IrwinID                             AS irwin_id,
            attr_POOState                            AS state,
            attr_POOCounty                           AS county,
            attr_GACC                                AS gacc,
            attr_FireCause                           AS fire_cause,
            attr_FireCauseGeneral                    AS fire_cause_general,
            attr_IncidentTypeCategory                AS incident_type_category,
            TRY_CAST(COALESCE(poly_GISAcres, attr_IncidentSize) AS DOUBLE) AS gis_acres,
            TRY_CAST(attr_FinalAcres AS DOUBLE)      AS final_acres,
            TRY_CAST(attr_PercentContained AS DOUBLE) AS percent_contained,
            TRY_CAST(attr_InitialLatitude AS DOUBLE)  AS latitude,
            TRY_CAST(attr_InitialLongitude AS DOUBLE) AS longitude,
            {_ts('attr_FireDiscoveryDateTime')}      AS fire_discovery_at,
            {_ts('attr_ContainmentDateTime')}        AS containment_at,
            {_ts('attr_FireOutDateTime')}            AS fire_out_at,
            {_ts('poly_DateCurrent')}                AS perimeter_date_current,
            attr_FireMgmtComplexity                  AS fire_mgmt_complexity,
            attr_IncidentComplexityLevel             AS incident_complexity_level
        FROM "{_PERIM}"
    ''',
    _INFORM: f'''
        SELECT
            UniqueFireIdentifier                     AS unique_fire_id,
            IncidentName                             AS incident_name,
            TRY_CAST(CalendarYear AS INTEGER)        AS calendar_year,
            {_ts('FireDiscoveryDateTime')}           AS fire_discovery_at,
            {_ts('ContainmentDateTime')}             AS containment_at,
            {_ts('FireOutDateTime')}                 AS fire_out_at,
            TRY_CAST(IncidentSize AS DOUBLE)         AS incident_size_acres,
            IncidentTypeCategory                     AS incident_type_category,
            GACC                                     AS gacc,
            POOState                                 AS state,
            POOCounty                                AS county,
            POOJurisdictionalAgency                  AS jurisdictional_agency,
            POOProtectingAgency                      AS protecting_agency,
            TRY_CAST(InitialLatitude AS DOUBLE)      AS latitude,
            TRY_CAST(InitialLongitude AS DOUBLE)     AS longitude,
            Status                                   AS status,
            FireCode                                 AS fire_code
        FROM "{_INFORM}"
    ''',
    _INCIDENTS: f'''
        SELECT
            UniqueFireIdentifier                     AS unique_fire_id,
            IncidentName                             AS incident_name,
            IrwinID                                  AS irwin_id,
            {_ts('FireDiscoveryDateTime')}           AS fire_discovery_at,
            {_ts('ContainmentDateTime')}             AS containment_at,
            {_ts('ControlDateTime')}                 AS control_at,
            {_ts('FireOutDateTime')}                 AS fire_out_at,
            TRY_CAST(IncidentSize AS DOUBLE)         AS incident_size_acres,
            TRY_CAST(DiscoveryAcres AS DOUBLE)       AS discovery_acres,
            TRY_CAST(FinalAcres AS DOUBLE)           AS final_acres,
            TRY_CAST(PercentContained AS DOUBLE)     AS percent_contained,
            FireCause                                AS fire_cause,
            FireCauseGeneral                         AS fire_cause_general,
            IncidentTypeCategory                     AS incident_type_category,
            IncidentTypeKind                         AS incident_type_kind,
            FireMgmtComplexity                       AS fire_mgmt_complexity,
            GACC                                     AS gacc,
            POOState                                 AS state,
            POOCounty                                AS county,
            POOJurisdictionalAgency                  AS jurisdictional_agency,
            POOProtectingAgency                      AS protecting_agency,
            TRY_CAST(InitialLatitude AS DOUBLE)      AS latitude,
            TRY_CAST(InitialLongitude AS DOUBLE)     AS longitude
        FROM "{_INCIDENTS}"
    ''',
    _VIIRS: f'''
        SELECT
            TRY_CAST(latitude AS DOUBLE)             AS latitude,
            TRY_CAST(longitude AS DOUBLE)            AS longitude,
            TRY_CAST(bright_ti4 AS DOUBLE)           AS brightness_ti4,
            TRY_CAST(bright_ti5 AS DOUBLE)           AS brightness_ti5,
            TRY_CAST(frp AS DOUBLE)                  AS fire_radiative_power,
            TRY_CAST(scan AS DOUBLE)                 AS scan,
            TRY_CAST(track AS DOUBLE)                AS track,
            {_ts('acq_date')}                        AS acquired_date,
            {_ts('esritimeutc')}                     AS acquired_at_utc,
            satellite                                AS satellite,
            confidence                               AS confidence,
            daynight                                 AS day_night,
            version                                  AS version,
            TRY_CAST(hours_old AS INTEGER)           AS hours_old
        FROM "{_VIIRS}"
    ''',
    _HISTORY: f'''
        SELECT
            UNQE_FIRE_ID                             AS unique_fire_id,
            IRWINID                                  AS irwin_id,
            INCIDENT                                 AS incident_name,
            TRY_CAST(FIRE_YEAR_INT AS INTEGER)       AS fire_year,
            TRY_CAST(GIS_ACRES AS DOUBLE)            AS gis_acres,
            UNIT_ID                                  AS unit_id,
            POO_RESP_I                               AS poo_responsible_unit,
            FEATURE_CA                               AS feature_category,
            MAP_METHOD                               AS map_method,
            AGENCY                                   AS agency,
            SOURCE                                   AS source,
            DATE_CUR                                 AS date_current
        FROM "{_HISTORY}"
    ''',
    _IMSR: f'''
        SELECT
            incident_id                              AS incident_id,
            fire_name                                AS fire_name,
            UniqueFireIdentifier                     AS unique_fire_id,
            IrwinID                                  AS irwin_id,
            TRY_CAST(latitude AS DOUBLE)             AS latitude,
            TRY_CAST(longitude AS DOUBLE)            AS longitude,
            TRY_CAST(size AS DOUBLE)                 AS size_acres,
            gacc                                     AS gacc,
            imt_type                                 AS imt_type,
            x100pct                                  AS contained_flag,
            {_ts('initial_imsr_date')}               AS initial_imsr_at,
            {_ts('intl_imsr_post_date')}             AS intl_imsr_post_at,
            post_year                                AS post_year,
            post_month                               AS post_month,
            Occurrence                               AS occurrence,
            TRY_CAST(nmbr_apprs AS INTEGER)          AS num_appearances
        FROM "{_IMSR}"
    ''',
    _GEOMAC: f'''
        SELECT
            uniquefireidentifier                     AS unique_fire_id,
            irwinid                                  AS irwin_id,
            incidentname                             AS incident_name,
            TRY_CAST(fireyear AS INTEGER)            AS fire_year,
            TRY_CAST(gisacres AS DOUBLE)             AS gis_acres,
            agency                                   AS agency,
            state                                    AS state,
            pooresponsibleunit                       AS poo_responsible_unit,
            complexname                              AS complex_name,
            firecode                                 AS fire_code,
            incomplex                                AS in_complex,
            {_ts('datecurrent')}                     AS date_current,
            {_ts('perimeterdatetime')}               AS perimeter_at
        FROM "{_GEOMAC}"
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_SQL[s.id])
    for s in DOWNLOAD_SPECS
]
