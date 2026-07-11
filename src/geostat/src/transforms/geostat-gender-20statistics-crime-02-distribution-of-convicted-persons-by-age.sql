-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    CAST("years" AS BIGINT) AS years,
    "age",
    "value"
FROM "geostat-gender-20statistics-crime-02-distribution-of-convicted-persons-by-age"
