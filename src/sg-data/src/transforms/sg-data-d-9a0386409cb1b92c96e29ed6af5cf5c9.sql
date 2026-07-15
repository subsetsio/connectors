-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "net_wdl_amt"
FROM "sg-data-d-9a0386409cb1b92c96e29ed6af5cf5c9"
