-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "project_number",
    "capital_plan",
    "agency_name",
    "plan_revision",
    "budget_submission_date",
    "project_descrition",
    "change_narrative",
    "plan_year_year_1_allocation",
    "plan_year_year_2_allocation",
    "plan_year_year_3_allocation",
    "plan_year_year_4_allocation",
    "plan_year_year_5_allocation",
    "out_years_allocation",
    "total_allocation"
FROM "mta-open-data-kizb-nxtu"
