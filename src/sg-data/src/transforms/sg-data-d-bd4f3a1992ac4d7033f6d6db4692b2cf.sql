-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "regrossed_bal_grp",
    "no_of_active_mbrs"
FROM "sg-data-d-bd4f3a1992ac4d7033f6d6db4692b2cf"
