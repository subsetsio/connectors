-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "total_no_of_water_customers",
    "no_of_customers_served_by_tankers",
    "percentage_of_customers_served_by_tankers",
    "reduction",
    "percentage_reduction"
FROM "qatar-planning-and-statistics-authority-statistics-of-customers-served-by-tankers"
