-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kind_of_economic_activity",
    "period",
    "value"
FROM "geostat-hotels-20and-20restaurants-accommodation-20and-20food-20service-20activities-20by-20kind-20of-20economic-20activity-20nace-20rev-2-total-20purchases-20of-20goods-20and-20services-total-purchases-by-kind-of-econ-act"
