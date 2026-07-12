-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "bank_nationality",
    "bank_nationality_ar",
    "gross_value_per_employee",
    "productivity_of_employee",
    "percentage_of_intermediate_services_to_output",
    "percentage_of_intermediate_goods_to_output",
    "average_annual_wage_1"
FROM "qatar-planning-and-statistics-authority-main-economic-indicators-by-bank-nationality"
