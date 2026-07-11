-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age",
    "sex",
    CAST("year" AS BIGINT) AS year,
    "causes_of_death_in_accordance_with_eurostat_standard",
    "value"
FROM "geostat-demography-deaths-23-5-deaths-by-causes-age-sex"
