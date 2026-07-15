-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "effective_from",
    "age_grp",
    "contributing_party",
    "contribution_rate"
FROM "sg-data-d-98ffa142ae0dec40391f78f81d26aca9"
