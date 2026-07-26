-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "series",
    "outstanding_principal_amount",
    "provider",
    "facility_type",
    "expiration",
    "remarketing_agent",
    "data_as_of"
FROM "nyc-open-data-xprg-trsi"
