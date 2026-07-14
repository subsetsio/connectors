-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Elasticity estimates are product-level parameters, not observed trade flows.
SELECT
    "HS6" AS hs6,
    "zero",
    "positive",
    "sigma"
FROM "cepii-product-level-trade-elasticities"
