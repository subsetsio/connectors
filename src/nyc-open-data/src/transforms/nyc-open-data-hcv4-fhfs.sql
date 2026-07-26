-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "neighborhood",
    "type_of_home",
    "number_of_sales",
    "lowest_sale_price",
    "average_sale_price",
    "median_sale_price",
    "highest_sale_price"
FROM "nyc-open-data-hcv4-fhfs"
