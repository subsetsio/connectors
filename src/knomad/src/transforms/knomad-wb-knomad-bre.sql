SELECT
    REF_AREA                                          AS country_code,
    REF_AREA_LABEL                                    AS country,
    REPLACE(COMP_BREAKDOWN_1, 'WB_KNOMAD_', '')       AS counterpart_code,
    COMP_BREAKDOWN_1_LABEL                            AS counterpart,
    CAST(TIME_PERIOD AS INTEGER)                      AS year,
    TRY_CAST(OBS_VALUE AS DOUBLE)                     AS remittance_usd_million,
    UNIT_MEASURE_LABEL                                        AS unit,
    INDICATOR_LABEL                                   AS indicator,
    OBS_STATUS                                        AS obs_status
FROM "knomad-wb-knomad-bre"
WHERE OBS_VALUE IS NOT NULL
  AND TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
  AND COMP_BREAKDOWN_1 NOT IN ('_T', '_Z')
  AND TRY_CAST(TIME_PERIOD AS INTEGER) IS NOT NULL
