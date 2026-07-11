-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reproduction_rates",
    "year",
    "value"
FROM "geostat-demography-births-18-gross-and-net-reproduction-rates"
