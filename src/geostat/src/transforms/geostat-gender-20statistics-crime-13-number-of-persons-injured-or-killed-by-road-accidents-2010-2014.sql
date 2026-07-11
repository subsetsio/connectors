-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "status",
    CAST("year" AS BIGINT) AS year,
    "region",
    "value"
FROM "geostat-gender-20statistics-crime-13-number-of-persons-injured-or-killed-by-road-accidents-2010-2014"
