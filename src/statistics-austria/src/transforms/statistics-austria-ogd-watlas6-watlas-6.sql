-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year_starting_1995" AS BIGINT) AS year_starting_1995,
    "nace",
    "federal_provinces",
    "number_of_establishments",
    "revenue_in_eur_million",
    "total_purchases_of_goods_and_services_in_eur_million",
    "gross_investments_in_tangible_goods_in_eur_million",
    "persons_employed",
    "employees",
    "wages_and_salaries_in_eur_million",
    "establishment_density_per_1_000_inhabitants",
    "revenue_of_establishments_per_establishment_in_eur",
    "revenue_of_establishments_per_person_employed_in_eur",
    "persons_employed_per_establishment",
    "gross_wages_and_salaries_per_employee_in_eur",
    "purchases_of_goods_and_services_in_of_revenue_of_establishments"
FROM "statistics-austria-ogd-watlas6-watlas-6"
