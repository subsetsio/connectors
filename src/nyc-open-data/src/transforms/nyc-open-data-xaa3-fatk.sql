-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "address_verification_id",
    "physical_address_id",
    "agency_id",
    "contract_id",
    "verification_date",
    "active"
FROM "nyc-open-data-xaa3-fatk"
