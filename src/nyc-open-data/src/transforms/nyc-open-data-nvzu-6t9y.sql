-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reporting_fiscal_year",
    "agency",
    "agency_name",
    "resource_indicators",
    "previous_fy_actual",
    "current_fy_plan",
    "current_fy_updated_plan",
    "next_fy_plan",
    "previous_fy_4month_actual",
    "current_fy_4month_actual",
    "notes"
FROM "nyc-open-data-nvzu-6t9y"
