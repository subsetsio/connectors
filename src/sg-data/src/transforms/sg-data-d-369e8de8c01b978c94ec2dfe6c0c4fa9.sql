-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "net_wdl_amt"
FROM "sg-data-d-369e8de8c01b978c94ec2dfe6c0c4fa9"
