-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "as_of_month",
    "age_groups",
    "count"
FROM "sg-data-d-abeeab6fb3b739d7b234e7452bafd07c"
