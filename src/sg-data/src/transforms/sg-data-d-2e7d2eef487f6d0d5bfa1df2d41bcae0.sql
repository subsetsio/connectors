-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "regrossed_bal_grp",
    "regrossed_bal_amt"
FROM "sg-data-d-2e7d2eef487f6d0d5bfa1df2d41bcae0"
