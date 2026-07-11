-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("years" AS BIGINT) AS years,
    "regions",
    "value"
FROM "geostat-demography-marriages-39-1-crude-marriage-rate-by-regions"
