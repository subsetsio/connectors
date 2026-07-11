-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "months",
    CAST("years" AS BIGINT) AS years,
    "cis_countries",
    "value"
FROM "geostat-external-20trade-exports-by-20countries-6-exports-cis-countries-1995-2019"
