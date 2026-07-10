-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year_starting_2021" AS BIGINT) AS year_starting_2021,
    "nace",
    "enterprise_size_classes",
    "number_of_enterprises",
    "persons_employed",
    "employees",
    "personnel_costs_in_eur_million",
    "turnover_in_eur_million",
    "total_purchases_of_goods_and_services_in_eur_million",
    "value_added_at_factor_cost_in_eur_million",
    "gross_investments_in_eur_million",
    "turnover_per_enterprise_in_eur",
    "turnover_per_person_employed_in_eur",
    "purchases_of_goods_and_services_in_of_turnover",
    "persons_employed_per_enterprise",
    "annual_personnel_expenditure_per_employee_in_eur",
    "personnel_expenditure_in_of_gross_value_added"
FROM "statistics-austria-ogd-watlas16-watlas-16"
