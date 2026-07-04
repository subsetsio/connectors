-- imf-isora-latest-data-pub: IMF SDMX 3.0 dataflow, long format (dimensions + period + value).
-- Measure 'OBSERVATION' cast to DOUBLE; non-numeric/empty observations dropped.
SELECT
  "JURISDICTION",
  "INDICATOR",
  "FREQUENCY",
  "TIME_PERIOD",
  TRY_CAST("OBSERVATION" AS DOUBLE) AS "OBS_VALUE"
FROM "imf-isora-latest-data-pub"
WHERE TRY_CAST("OBSERVATION" AS DOUBLE) IS NOT NULL
