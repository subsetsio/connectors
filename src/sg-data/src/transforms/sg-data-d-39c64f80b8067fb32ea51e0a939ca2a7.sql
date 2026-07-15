-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "length_of_service",
    "executive_level",
    "public_service_sector",
    "year",
    "outflow_count"
FROM "sg-data-d-39c64f80b8067fb32ea51e0a939ca2a7"
