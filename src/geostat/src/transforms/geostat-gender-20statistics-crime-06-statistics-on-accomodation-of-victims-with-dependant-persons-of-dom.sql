-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    CAST("year" AS BIGINT) AS year,
    "permanent_residence",
    "value"
FROM "geostat-gender-20statistics-crime-06-statistics-on-accomodation-of-victims-with-dependant-persons-of-dom"
