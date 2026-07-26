-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "fiscal_year",
    "agency_number",
    "agency_name",
    "unit_appropriation_number",
    "unit_appropriation_name",
    "personal_serviceother_than_personal_service_indicator",
    "total_financial_plan_amount",
    "total_adopted_budget_amount",
    "total_current_budget_amount",
    "federal_funds_financial_plan_amount",
    "federal_funds_adopted_budget_amount",
    "federal_funds_current_budget_amount",
    "state_funds_financial_plan_amount",
    "state_funds_adopted_budget_amount",
    "state_funds_current_budget_amount",
    "interfund_agreement_funds_financial_plan_amount",
    "interfund_agreement_funds_adopted_budget_amount",
    "interfund_agreement_funds_current_budget_amount",
    "intracity_sales_funds_financial_plan_amount",
    "intracity_sales_funds_adopted_budget_amount",
    "intracity_sales_funds_current_budget_amount",
    "other_categorical_funds_financial_plan_amount",
    "other_categorical_funds_adopted_budget_amount",
    "other_categorical_funds_current_budget_amount",
    "community_development_funds_financial_plan_amount",
    "community_development_funds_adopted_budget_amount",
    "community_development_funds_current_budget_amount",
    "city_funds_financial_plan_amount",
    "city_funds_adopted_budget_amount",
    "city_funds_current_budget_amount"
FROM "nyc-open-data-39g5-gbp3"
