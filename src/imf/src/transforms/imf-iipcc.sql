-- imf-iipcc: IMF SDMX 3.0 dataflow, long format (dimensions + period + value).
-- Measure 'OBS_VALUE' cast to DOUBLE; non-numeric/empty observations dropped.
SELECT
  "COUNTRY",
  "BOP_ACCOUNTING_ENTRY",
  "INDICATOR",
  "CURRENCY",
  "UNIT",
  "FREQUENCY",
  "TIME_PERIOD",
  TRY_CAST("OBS_VALUE" AS DOUBLE) AS "OBS_VALUE"
FROM "imf-iipcc"
WHERE TRY_CAST("OBS_VALUE" AS DOUBLE) IS NOT NULL
