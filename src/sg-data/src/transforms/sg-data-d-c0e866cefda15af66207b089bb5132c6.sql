-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "length_of_service",
    "executive_level",
    "public_service_sector",
    "year",
    "staff_strength"
FROM "sg-data-d-c0e866cefda15af66207b089bb5132c6"
