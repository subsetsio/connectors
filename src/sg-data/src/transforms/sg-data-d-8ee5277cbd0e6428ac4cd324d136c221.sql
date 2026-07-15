-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "housing_schm_type",
    "net_wdl_amt"
FROM "sg-data-d-8ee5277cbd0e6428ac4cd324d136c221"
