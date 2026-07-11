-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    CAST("period" AS BIGINT) AS period,
    "value"
FROM "geostat-trade-wholesale-20and-20retail-20trade-2c-20repair-20of-20motor-20vehicles-20and-20motorcycles-purchases-20of-20goods-20and-20services-20for-20resale-purchases-for-resale-by-regions"
