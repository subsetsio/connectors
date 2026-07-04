-- imf-gs-li: IMF SDMX 3.0 dataflow, long format (dimensions + period + value).
-- Measure 'OBS_VALUE' cast to DOUBLE; non-numeric/empty observations dropped.
SELECT
  "COUNTRY",
  "GENDER",
  "INDICATOR",
  "GS_MS",
  "GS_LI_DS",
  "GS_LI_EA",
  "GS_LI_ED",
  "GS_LI_OCC",
  "AGE_GROUP",
  "AGGREGATION_TYPE",
  "FREQUENCY",
  "TIME_PERIOD",
  TRY_CAST("OBS_VALUE" AS DOUBLE) AS "OBS_VALUE"
FROM "imf-gs-li"
WHERE TRY_CAST("OBS_VALUE" AS DOUBLE) IS NOT NULL
