-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This organogram combines senior and junior staff resources; filter by source resource and grade-related fields before treating rows as a single staff-role population.
SELECT
    "resource_name",
    "resource_id",
    CAST("resource_last_modified" AS TIMESTAMP) AS resource_last_modified,
    "source_url",
    "row_index",
    "actual_pay_ceiling",
    "actual_pay_floor",
    "contact_e_mail",
    "contact_phone",
    CAST("fte" AS DOUBLE) AS fte,
    "generic_job_title",
    "grade",
    "grade_or_equivalent",
    "job_team_function",
    "job_title",
    "name",
    "notes",
    CAST("number_of_posts_in_fte" AS DOUBLE) AS number_of_posts_in_fte,
    "office_region",
    "organisation",
    "parent_department",
    CAST("payscale_maximum" AS BIGINT) AS payscale_maximum,
    CAST("payscale_minimum" AS BIGINT) AS payscale_minimum,
    "post_unique_reference",
    "professional_occupational_group",
    "reporting_senior_post",
    "reports_to_senior_post",
    "salary_cost_of_reports",
    "unit",
    CAST("valid" AS DOUBLE) AS valid
FROM "uk-dwp-organogram-of-staff-roles-salaries30092019"
