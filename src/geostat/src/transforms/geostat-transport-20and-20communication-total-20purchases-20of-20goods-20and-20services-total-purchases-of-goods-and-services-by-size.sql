-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "enterprise_size",
    "period",
    "value"
FROM "geostat-transport-20and-20communication-total-20purchases-20of-20goods-20and-20services-total-purchases-of-goods-and-services-by-size"
