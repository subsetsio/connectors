-- imf-cci: IMF SDMX 3.0 dataflow, long format (dimensions + period + value).
-- Measure 'OBS_VALUE' cast to DOUBLE; non-numeric/empty observations dropped.
SELECT
  "COUNTRY",
  "INDICATOR",
  "GEOGRAPHIC_MARINE_ZONES_AND_CLIMATIC_CLASSIFICATIONS",
  "FREQUENCY",
  "TIME_PERIOD",
  TRY_CAST("OBS_VALUE" AS DOUBLE) AS "OBS_VALUE"
FROM "imf-cci"
WHERE TRY_CAST("OBS_VALUE" AS DOUBLE) IS NOT NULL
