-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "percentage_of_female_adults_who_support_increasing_taxes_on_tobacco_products",
    "percentage_of_male_adults_who_support_increasing_taxes_on_tobacco_products",
    "percentage_overall_of_adults_who_support_increasing_taxes_on_tobacco_products"
FROM "qatar-planning-and-statistics-authority-percentage-of-adults-who-support-increasing-taxes-on-tobacco-products-by-gender-and-nationality"
