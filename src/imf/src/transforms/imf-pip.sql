-- imf-pip: IMF SDMX 3.0 dataflow, long format (dimensions + period + value).
-- Measure 'OBS_VALUE' cast to DOUBLE; non-numeric/empty observations dropped.
SELECT
  "COUNTRY",
  "ACCOUNTING_ENTRY",
  "INDICATOR",
  "SECTOR",
  "COUNTERPART_SECTOR",
  "COUNTERPART_COUNTRY",
  "FREQUENCY",
  "TIME_PERIOD",
  TRY_CAST("OBS_VALUE" AS DOUBLE) AS "OBS_VALUE"
FROM "imf-pip"
WHERE TRY_CAST("OBS_VALUE" AS DOUBLE) IS NOT NULL
