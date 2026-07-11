-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "education_level",
    "value"
FROM "geostat-gender-20statistics-crime-08-number-of-persons-in-shelters-for-human-trafficking-and-victims-of-domestic"
