-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year_starting_2021" AS BIGINT) AS year_starting_2021,
    "nace",
    "federal_provinces",
    "number_of_local_units",
    "turnover_in_eur_million",
    "value_added_in_eur_million",
    "gross_investments_in_tangible_goods_in_eur_million",
    "persons_employed",
    "employees",
    "gross_wages_and_salaries_in_eur_million",
    "purchase_of_goods_and_services",
    "local_unit_density_per_1_000_inhabitants",
    "turnover_per_local_unit_in_eur",
    "turnover_per_person_employed_in_eur",
    "persons_employed_per_local_unit",
    "gross_wages_and_salaries_per_employee_in_eur",
    "purchase_of_goods_and_services_2"
FROM "statistics-austria-ogd-watlas18-watlas-18"
