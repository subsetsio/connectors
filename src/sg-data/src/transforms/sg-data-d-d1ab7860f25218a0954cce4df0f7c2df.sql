-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "regrossed_bal_grp",
    "regrossed_bal_amt"
FROM "sg-data-d-d1ab7860f25218a0954cce4df0f7c2df"
