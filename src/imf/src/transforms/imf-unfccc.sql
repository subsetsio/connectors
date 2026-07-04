-- imf-unfccc: IMF SDMX 3.0 dataflow, long format (dimensions + period + value).
-- Measure 'OBS_VALUE' cast to DOUBLE; non-numeric/empty observations dropped.
SELECT
  "COUNTRY",
  "INDUSTRY",
  "INDICATOR",
  "GAS_TYPE",
  "TYPE_OF_TRANSFORMATION",
  "FREQUENCY",
  "TIME_PERIOD",
  TRY_CAST("OBS_VALUE" AS DOUBLE) AS "OBS_VALUE"
FROM "imf-unfccc"
WHERE TRY_CAST("OBS_VALUE" AS DOUBLE) IS NOT NULL
