-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "eenterprise_size",
    "period",
    "value"
FROM "geostat-transport-20and-20communication-personel-20cost-personnel-costs-by-size-of-enterp"
