-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender_of_holder",
    CAST("years" AS BIGINT) AS years,
    "land_type",
    "value"
FROM "geostat-gender-20statistics-agriculture-2-distribution-of-land-area"
