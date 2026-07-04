-- imf-qnea: IMF SDMX 3.0 dataflow, long format (dimensions + period + value).
-- Measure 'OBS_VALUE' cast to DOUBLE; non-numeric/empty observations dropped.
SELECT
  "COUNTRY",
  "INDICATOR",
  "PRICE_TYPE",
  "S_ADJUSTMENT",
  "TYPE_OF_TRANSFORMATION",
  "FREQUENCY",
  "TIME_PERIOD",
  TRY_CAST("OBS_VALUE" AS DOUBLE) AS "OBS_VALUE"
FROM "imf-qnea"
WHERE TRY_CAST("OBS_VALUE" AS DOUBLE) IS NOT NULL
