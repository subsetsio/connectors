-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "executive_level",
    "public_service_sector",
    "year",
    "inflow_count"
FROM "sg-data-d-b1c25988c2cea189f27fd0e824716dae"
