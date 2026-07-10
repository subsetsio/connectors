-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: NMDB rows are aggregate statistics by market, geography, period, and series; value1 and value2 are series-specific measures and should not be summed across seriesid.
SELECT
    "source",
    "frequency",
    "geolevel",
    "geoid",
    "geoname",
    "market",
    "period",
    CAST("year" AS BIGINT) AS year,
    CAST("quarter" AS BIGINT) AS quarter,
    CAST("month" AS BIGINT) AS month,
    CAST("suppressed" AS BIGINT) AS suppressed,
    "seriesid",
    CAST("value1" AS DOUBLE) AS value1,
    "value2"
FROM "fhfa-nmdb-aggregate-statistics"
