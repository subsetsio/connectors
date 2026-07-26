-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "time_period",
    "food_product_group",
    "food_product_category",
    "product_name",
    "product_type",
    "origin_detail",
    "distributor",
    "vendor",
    "of_units",
    "total_weight_in_lbs",
    "total_cost"
FROM "nyc-open-data-usrf-za7k"
