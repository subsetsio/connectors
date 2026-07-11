-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "activity",
    "value"
FROM "geostat-national-20accounts-system-20of-20national-20accounts-202008-20-28sna-202008-29-gross-20domestic-20product-20-28gdp-29-14-non-observed-va"
