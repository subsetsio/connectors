SELECT
    REF_AREA                            AS country_code,
    REF_AREA_LABEL                      AS country,
    CAST(TIME_PERIOD AS INTEGER)        AS year,
    TRY_CAST(OBS_VALUE AS DOUBLE)       AS value_usd_million,
    UNIT_MEASURE_LABEL                  AS unit,
    INDICATOR_LABEL                     AS indicator,
    OBS_STATUS                          AS obs_status
FROM "knomad-wb-knomad-mro"
WHERE OBS_VALUE IS NOT NULL
  AND TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
  AND TRY_CAST(TIME_PERIOD AS INTEGER) IS NOT NULL
