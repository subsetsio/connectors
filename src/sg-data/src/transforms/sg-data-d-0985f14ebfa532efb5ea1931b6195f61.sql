-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "age_grp",
    "gender",
    "net_bal_amt"
FROM "sg-data-d-0985f14ebfa532efb5ea1931b6195f61"
