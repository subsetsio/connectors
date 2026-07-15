-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "executive_level",
    "public_service_sector",
    "year",
    "staff_strength"
FROM "sg-data-d-8b7ca60d610db92a752565f153af4b6a"
