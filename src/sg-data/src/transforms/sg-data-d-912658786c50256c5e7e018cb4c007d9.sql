-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "highest_educational_qualification",
    "executive_level",
    "public_service_sector",
    "year",
    "staff_strength"
FROM "sg-data-d-912658786c50256c5e7e018cb4c007d9"
