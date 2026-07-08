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
FROM "nifc-e02b85c0ea784ce7bd8add7ae3d293d0-0"
