-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_reported_as_of",
    "pid",
    "project_name",
    "description",
    "category",
    "borough",
    "managing_agency",
    "client_agency",
    "current_phase",
    "design_start",
    "budget_forecast",
    "latest_budget_changes",
    "total_budget_changes",
    "forecast_completion",
    "latest_schedule_changes",
    "total_schedule_changes"
FROM "nyc-open-data-n7gv-k5yt"
