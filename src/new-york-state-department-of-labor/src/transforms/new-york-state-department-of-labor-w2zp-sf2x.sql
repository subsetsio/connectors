-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Certified payroll registration rows do not expose a stable row identifier; treat them as reported payroll records and aggregate only after choosing project, week, work category, and job title dimensions.
SELECT
    "account",
    "project_name",
    "prc_number",
    "work_category",
    CAST("week_ending_date" AS TIMESTAMP) AS week_ending_date,
    CAST("st_total_hours" AS DOUBLE) AS st_total_hours,
    CAST("ot_total_hours" AS DOUBLE) AS ot_total_hours,
    CAST("st_hourly_rate" AS DOUBLE) AS st_hourly_rate,
    CAST("ot_hourly_rate" AS DOUBLE) AS ot_hourly_rate,
    CAST("wages" AS DOUBLE) AS wages,
    "job_title",
    CAST("project_start_date" AS TIMESTAMP) AS project_start_date,
    CAST("project_end_date" AS TIMESTAMP) AS project_end_date,
    "project_street_1",
    "project_street_2",
    "project_city",
    "project_state",
    "project_zipcode",
    "project_status",
    "department_of_jurisdiction"
FROM "new-york-state-department-of-labor-w2zp-sf2x"
