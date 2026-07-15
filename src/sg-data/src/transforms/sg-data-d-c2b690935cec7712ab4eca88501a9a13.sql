-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "executive_level",
    "public_service_sector",
    "year",
    "outflow_count"
FROM "sg-data-d-c2b690935cec7712ab4eca88501a9a13"
