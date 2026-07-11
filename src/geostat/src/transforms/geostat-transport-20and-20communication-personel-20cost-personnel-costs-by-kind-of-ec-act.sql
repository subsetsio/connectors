-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kind_of_conomic_activity",
    "period",
    "value"
FROM "geostat-transport-20and-20communication-personel-20cost-personnel-costs-by-kind-of-ec-act"
