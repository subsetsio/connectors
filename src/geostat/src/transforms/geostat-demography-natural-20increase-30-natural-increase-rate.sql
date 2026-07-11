-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rate",
    "year",
    "value"
FROM "geostat-demography-natural-20increase-30-natural-increase-rate"
