-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "effective_from",
    "age_grp",
    "account_type",
    "allocation_rate"
FROM "sg-data-d-97ec9a2ce15cbf253128e48779a3fba0"
