-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "urban_rural",
    CAST("year" AS BIGINT) AS year,
    "gender_of_household_head",
    "value"
FROM "geostat-gender-20statistics-households-02-distribution-of-households-by-gender-of-head-of-household-in-urban-an"
