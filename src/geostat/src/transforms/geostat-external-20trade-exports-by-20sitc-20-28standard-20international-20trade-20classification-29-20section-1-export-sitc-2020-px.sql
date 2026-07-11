-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "months",
    CAST("years" AS BIGINT) AS years,
    "sitc_section",
    "value"
FROM "geostat-external-20trade-exports-by-20sitc-20-28standard-20international-20trade-20classification-29-20section-1-export-sitc-2020-px"
