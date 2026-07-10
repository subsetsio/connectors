-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "provinces",
    "all_economic_activities",
    "all_legal_forms_grouped",
    "all_employee_size_classes",
    "gender_total",
    "active_enterprises",
    "employed_persons_in_active_enterprises",
    "employees_in_active_enterprises",
    "enterprise_births",
    "employed_persons_in_enterprise_births",
    "employees_in_enterprise_births",
    "enterprise_deaths",
    "employed_persons_in_enterprise_deaths",
    "employees_in_enterprise_deaths"
FROM "statistics-austria-ogd-reg-udemo-neu-ud-ogd-2"
