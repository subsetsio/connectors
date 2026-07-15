-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_name",
    "moe_programme_desc"
FROM "sg-data-d-b0697d22a7837a4eddf72efb66a36fc2"
