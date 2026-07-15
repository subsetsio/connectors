-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "age_grp",
    "sex",
    "net_bal_amt"
FROM "sg-data-d-a0982d560463c45e990efef8bb1b4ee5"
