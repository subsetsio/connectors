-- imf-gs-health: IMF SDMX 3.0 dataflow, long format (dimensions + period + value).
-- Measure 'OBS_VALUE' cast to DOUBLE; non-numeric/empty observations dropped.
SELECT
  "COUNTRY",
  "GENDER",
  "INDICATOR",
  "AGE_GROUP",
  "AGGREGATION_TYPE",
  "FREQUENCY",
  "TIME_PERIOD",
  TRY_CAST("OBS_VALUE" AS DOUBLE) AS "OBS_VALUE"
FROM "imf-gs-health"
WHERE TRY_CAST("OBS_VALUE" AS DOUBLE) IS NOT NULL
