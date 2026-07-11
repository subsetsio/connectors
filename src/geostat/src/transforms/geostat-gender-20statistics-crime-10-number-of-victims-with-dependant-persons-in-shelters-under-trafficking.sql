-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "age",
    "value"
FROM "geostat-gender-20statistics-crime-10-number-of-victims-with-dependant-persons-in-shelters-under-trafficking"
