-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "migrants",
    CAST("year" AS BIGINT) AS year,
    "citizenship",
    "value"
FROM "geostat-demography-migration-33-number-of-immigrants-and-emigrants-by-sex-and-citizenship"
