-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reporting_fiscal_year",
    "agency_code",
    "agency",
    "agency_name",
    "unit_of_appropriation",
    "appropriation_type",
    "expenditures_previous_fy_000000",
    "modified_budget_current_fy_000000",
    "applicable_mmr_goals",
    "notes"
FROM "nyc-open-data-2jrp-puwz"
