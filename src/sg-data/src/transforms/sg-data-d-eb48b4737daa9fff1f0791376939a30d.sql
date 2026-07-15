-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Owner" AS owner,
    "Tenant" AS tenant,
    "Others" AS others
FROM "sg-data-d-eb48b4737daa9fff1f0791376939a30d"
