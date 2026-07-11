-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "end_of_quarter",
    "outstanding_loans",
    "outstanding_loans_ratio",
    "outstanding_loans_amt",
    "outstanding_loans_amt_ratio",
    "unsecured_portion_amt",
    "lv_ratio"
FROM "hkma-residential-mortgage-negative-equity"
