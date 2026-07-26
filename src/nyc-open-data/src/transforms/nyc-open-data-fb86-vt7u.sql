-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reporting_period",
    "managing_agency",
    "sponsor_agency",
    "pid",
    "fms_id",
    "total_budget",
    "spend_to_date",
    "spend_to_date_1",
    "fms_project_name",
    "agency_project_name",
    "agency_project_description",
    "current_phase",
    "current_phase_start",
    "forecast_current_phase_end",
    "forecast_completion",
    "actual_design_start",
    "actual_design_end",
    "actual_construction_procurement_start",
    "actual_construction_procurement_end",
    "actual_construction_start",
    "actual_construction_end",
    "borough",
    "community_board",
    "budget_line",
    "ten_year_plan_category",
    "agency_data_date",
    "fms_data_date"
FROM "nyc-open-data-fb86-vt7u"
