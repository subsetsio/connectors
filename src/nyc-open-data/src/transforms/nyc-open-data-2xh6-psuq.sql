-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "project_geographic_district",
    "project_building_identifier",
    "project_school_name",
    "project_type",
    "project_description",
    "project_phase_name",
    "project_status_name",
    "project_phase_actual_start_date",
    "project_phase_planned_end_date",
    "project_phase_actual_end_date",
    "project_budget_amount",
    "final_estimate_of_actual_costs_through_end_of_phase_amount",
    "total_phase_actual_spending_amount",
    "dsf_numbers"
FROM "nyc-open-data-2xh6-psuq"
