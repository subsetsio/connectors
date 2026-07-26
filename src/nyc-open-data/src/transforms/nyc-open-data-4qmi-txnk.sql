-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reporting_fiscal_year",
    "agency",
    "agency_name",
    "resource_indicators",
    "current_fy_projected_actual_not_yet_finalized",
    "current_fy_authorized_budget_level",
    "next_fy_authorized_budget_level",
    "_5yr_trend" AS 5yr_trend,
    "notes"
FROM "nyc-open-data-4qmi-txnk"
