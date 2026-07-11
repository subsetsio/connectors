-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "area",
    CAST("year" AS BIGINT) AS year,
    "threshold",
    "value"
FROM "geostat-social-20statistics-living-20conditions-2c-20subsistence-20minimum-relative-poverty"
