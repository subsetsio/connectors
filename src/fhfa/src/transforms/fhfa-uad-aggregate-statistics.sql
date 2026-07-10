-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: UAD rows are aggregate appraisal statistics by geography, purpose, time, series, and category; suppressed rows and different seriesid values are not additive measures.
SELECT
    "source",
    "appraisalsource",
    "series",
    "seriesid",
    "frequency",
    "geolevel",
    "geoname",
    "statepostal",
    "statefips",
    "fips",
    "tract",
    "metro",
    "purpose",
    CAST("year" AS BIGINT) AS year,
    CAST("quarter" AS BIGINT) AS quarter,
    "characteristic1",
    "category1",
    CAST("suppressed" AS BIGINT) AS suppressed,
    "value"
FROM "fhfa-uad-aggregate-statistics"
