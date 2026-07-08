SELECT * EXCLUDE (OBS_VALUE, DATAFLOW),
       TRY_CAST(OBS_VALUE AS DOUBLE) AS obs_value
FROM "un-statistics-division-df-undata-energybalance"
WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
