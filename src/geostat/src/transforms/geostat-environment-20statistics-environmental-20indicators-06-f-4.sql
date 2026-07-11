-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "pesticide_consumption_import_minus_export",
    "value"
FROM "geostat-environment-20statistics-environmental-20indicators-06-f-4"
