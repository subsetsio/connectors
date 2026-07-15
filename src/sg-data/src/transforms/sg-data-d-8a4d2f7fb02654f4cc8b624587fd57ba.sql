-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "broad_cause_group",
    "percentage"
FROM "sg-data-d-8a4d2f7fb02654f4cc8b624587fd57ba"
