-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    CAST("year" AS BIGINT) AS year,
    "permanent_residence",
    "value"
FROM "geostat-gender-20statistics-crime-09-number-of-persons-in-shelters-victims-of-human-trafficking"
