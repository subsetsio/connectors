-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "regions",
    CAST("period" AS BIGINT) AS period,
    "value"
FROM "geostat-trade-wholesale-20and-20retail-20trade-2c-20repair-20of-20motor-20vehicles-20and-20motorcycles-number-20of-20employees-number-of-employees-by-regions"
