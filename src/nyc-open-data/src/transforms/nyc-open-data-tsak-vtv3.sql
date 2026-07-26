-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "upcoming_project_design_number",
    "upcoming_project_name",
    "upcoming_project_borough",
    "upcoming_project_geographic_district",
    "upcoming_project_description",
    "upcoming_project_budget_range",
    "upcoming_project_design_completion_date",
    "upcoming_project_category",
    "upcoming_project_status"
FROM "nyc-open-data-tsak-vtv3"
