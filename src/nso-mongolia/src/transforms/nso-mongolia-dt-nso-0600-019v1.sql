-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Region" AS region,
    "Goods and services" AS goods_and_services,
    strptime("Month", '%Y-%m')::DATE AS month,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0600-019v1"
