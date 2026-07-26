-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "building_class_category",
    "number_of_sales",
    "minimum_sale_price",
    "average_sale_price",
    "median_sale_price",
    "maximum_sale_price"
FROM "nyc-open-data-hdu7-ujt4"
