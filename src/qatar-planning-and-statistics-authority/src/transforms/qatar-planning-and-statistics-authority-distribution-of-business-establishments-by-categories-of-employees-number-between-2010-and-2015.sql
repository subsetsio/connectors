-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "categories_of_employees_number",
    "fy_t_dd_lmshtglyn",
    "dd_lmshtglyn_fy_t_dd_2010_number_of_employees_in_census_2010",
    "dd_lmshtglyn_fy_t_dd_2015_number_of_employees_in_census_2015",
    "increase_percentage_during_the_period"
FROM "qatar-planning-and-statistics-authority-distribution-of-business-establishments-by-categories-of-employees-number-between-2010-and-2015"
