-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "no_of_members"
FROM "sg-data-d-11967e75a7e9a01d86fa5bac696fd24e"
