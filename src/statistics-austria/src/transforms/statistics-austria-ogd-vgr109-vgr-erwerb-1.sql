-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_series",
    "main_aggregates_of_national_accounts",
    "adjustment",
    "jobs_total_employment_by_industry_in_1000",
    "jobs_employees_in_1000",
    "jobs_self_employed_by_industry_in_1000",
    "persons_total_employment_by_industry_in_1000",
    "persons_employees_by_industry_in_1000",
    "persons_self_employed_by_industry_in_1000",
    "total_hours_worked_total_in_mil_hours",
    "total_hours_worked_employees_in_mil_hours",
    "total_hours_worked_self_employed_by_industry_in_mil_hours"
FROM "statistics-austria-ogd-vgr109-vgr-erwerb-1"
