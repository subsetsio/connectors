-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "housing_schm_type",
    "net_wdl_amt"
FROM "sg-data-d-7cce20f5d2d8ae2582da809e66a1cdd7"
