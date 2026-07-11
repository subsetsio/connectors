-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "previous_country_of_citizenship",
    "value"
FROM "geostat-demography-migration-49-8-citizenship-acquisition-by-citizenship"
