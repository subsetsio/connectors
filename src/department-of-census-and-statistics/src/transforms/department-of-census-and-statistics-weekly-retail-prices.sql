-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "week_label",
    "product",
    "product_name",
    "category",
    "price_lkr"
FROM "department-of-census-and-statistics-weekly-retail-prices"
