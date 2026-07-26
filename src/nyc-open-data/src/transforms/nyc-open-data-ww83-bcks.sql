-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "procurement_name",
    "procurement_industry",
    "nigp_codes",
    "mwbe_small_purchase_method"
FROM "nyc-open-data-ww83-bcks"
