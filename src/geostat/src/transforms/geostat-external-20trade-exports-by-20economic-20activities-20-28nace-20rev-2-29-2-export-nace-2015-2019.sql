-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "months",
    CAST("years" AS BIGINT) AS years,
    "nace_section",
    "value"
FROM "geostat-external-20trade-exports-by-20economic-20activities-20-28nace-20rev-2-29-2-export-nace-2015-2019"
