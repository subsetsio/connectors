-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "executive_level",
    "public_service_sector",
    "year",
    "staff_strength"
FROM "sg-data-d-b6c936cf4666cb00b5f4cba57eeef713"
