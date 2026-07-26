-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reporting_period",
    "managing_agency",
    "pid",
    "agency_project_name",
    "current_phase",
    "completion_date",
    "completion_date_type",
    "variance_day",
    "reason_for_forecast_completion_change",
    "data_date"
FROM "nyc-open-data-95tx-snak"
