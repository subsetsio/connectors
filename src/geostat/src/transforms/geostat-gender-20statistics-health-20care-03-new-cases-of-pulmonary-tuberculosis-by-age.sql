-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "age",
    CAST("year" AS BIGINT) AS year,
    "type",
    "value"
FROM "geostat-gender-20statistics-health-20care-03-new-cases-of-pulmonary-tuberculosis-by-age"
