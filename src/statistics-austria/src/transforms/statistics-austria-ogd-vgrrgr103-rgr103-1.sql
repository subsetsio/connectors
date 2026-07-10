-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "nuts3_units",
    "nace_2008",
    "gross_value_added_at_basic_prices_current_prices_in_million_euro",
    "compensation_of_employees_current_prices_in_million_euro",
    "gross_fixed_capital_formation_current_prices_in_million_euro",
    "employment_jobs_in_1000",
    "employees_jjobs_in_1000",
    "employees_total_hours_worked_in_million",
    "employment_total_hours_worked_in_million",
    "self_employees_total_hours_worked_in_million",
    "self_employees_jobs_in_1000",
    "employees_persons_in_1000",
    "employment_persons_in_1000",
    "self_employees_persons_in_1000"
FROM "statistics-austria-ogd-vgrrgr103-rgr103-1"
