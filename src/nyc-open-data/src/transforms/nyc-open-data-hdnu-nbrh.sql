-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "property",
    "personal_income_total",
    "less_transfers_to_debt_service_funds_and_adjustments",
    "personal_income_general_fund_revenue",
    "general_sales",
    "general_corporation",
    "financial_corporation",
    "unincorporated_business_income",
    "mortgage_recording",
    "commercial_rent",
    "conveyance_of_real_property",
    "other_taxes",
    "total_taxes"
FROM "nyc-open-data-hdnu-nbrh"
