-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "change_order_type",
    "agency",
    "count",
    "original_contract_value",
    "change_order_contract_value",
    "change_order_contract_in_fiscal_year",
    "days_processing_in_fiscal_year"
FROM "nyc-open-data-a2w2-wg79"
