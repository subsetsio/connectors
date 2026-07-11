-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "regions",
    CAST("period" AS BIGINT) AS period,
    "value"
FROM "geostat-industry-industry-20by-20kind-20of-20economic-20activity-20nace-20rev-2-personnel-20costs-personnel-costs-by-regions"
