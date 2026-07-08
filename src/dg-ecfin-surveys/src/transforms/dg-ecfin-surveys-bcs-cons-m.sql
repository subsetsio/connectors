SELECT
    * EXCLUDE (DATAFLOW, "LAST UPDATE", TIME_PERIOD, OBS_VALUE),
    TIME_PERIOD               AS time_period,
    TRY_CAST(OBS_VALUE AS DOUBLE) AS obs_value,
    "LAST UPDATE"             AS last_update
FROM "dg-ecfin-surveys-bcs-cons-m"
WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
