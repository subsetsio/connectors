-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "investment_schm_type",
    "net_wdl_amt"
FROM "sg-data-d-ee5f1fc9291821595831ce2e831e3f39"
