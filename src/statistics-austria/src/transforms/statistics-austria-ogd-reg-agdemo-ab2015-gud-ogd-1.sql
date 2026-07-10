-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "all_economic_activities",
    "all_legal_forms_grouped",
    "gender_total",
    "all_employee_size_classes",
    "provinces",
    "active_employer_enterprises",
    "employed_persons_in_active_employer_enterprises",
    "employees_in_active_employer_enterprises",
    "employer_enterprise_births",
    "employed_persons_in_employer_enterprise_births",
    "employees_in_employer_enterprise_births",
    "employer_enterprise_deaths",
    "employed_persons_in_employer_enterprise_deaths",
    "employees_in_employer_enterprise_deaths"
FROM "statistics-austria-ogd-reg-agdemo-ab2015-gud-ogd-1"
