-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "net_wdl_amt"
FROM "sg-data-d-a1c3c5620b8095c32dfee7a4f6601a36"
