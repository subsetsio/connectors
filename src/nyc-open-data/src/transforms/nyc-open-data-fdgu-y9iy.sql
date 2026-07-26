-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "fiscal_year",
    "agency_code",
    "agency_name",
    "ps_otps_indicator",
    "category_name",
    "subcategory_name",
    "adopted_budget_amount",
    "current_modified_budget_amount",
    "financial_plan_amount"
FROM "nyc-open-data-fdgu-y9iy"
