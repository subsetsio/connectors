-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "precipitation_categories",
    CAST("year" AS BIGINT) AS year,
    "locations",
    "value"
FROM "geostat-environment-20statistics-environmental-20indicators-b-2-atmospheric-precipitation"
