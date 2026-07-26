-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "condo_base_boro",
    "condo_base_block",
    "condo_base_lot",
    "condo_base_bbl",
    "condo_base_bbl_key",
    "condo_key",
    "condo_number",
    "condo_name",
    "condo_billing_bbl"
FROM "nyc-open-data-p8u6-a6it"
