-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "regrossed_bal_grp",
    "age_grp",
    "no_of_active_mbrs"
FROM "sg-data-d-6d7b9a8c80526f08a49b585f0e2c92e8"
