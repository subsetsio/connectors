-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "service_id",
    "organization_id",
    "_name" AS name,
    "status"
FROM "nyc-open-data-u4ef-3s9d"
