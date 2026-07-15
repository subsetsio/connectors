-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "executive_level",
    "public_service_sector",
    "year",
    "staff_strength"
FROM "sg-data-d-906df66867223c65d5a4d23b3fa61299"
