-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "months",
    CAST("years" AS BIGINT) AS years,
    "bec_broad_economic_categories",
    "value"
FROM "geostat-external-20trade-exports-by-20bec-20-28broad-20economic-20categories-29-1-export-bec-2020-px"
