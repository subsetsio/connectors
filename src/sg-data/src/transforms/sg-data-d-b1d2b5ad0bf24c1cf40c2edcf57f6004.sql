-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "Owner" AS owner,
    "Tenant" AS tenant,
    "Others" AS others
FROM "sg-data-d-b1d2b5ad0bf24c1cf40c2edcf57f6004"
