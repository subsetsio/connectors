-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "company_name",
    "license_type",
    "activity_type",
    "dosage_form",
    "expiry_date"
FROM "sg-data-d-bf50ce0f3f42f69d7acd50635afa62da"
