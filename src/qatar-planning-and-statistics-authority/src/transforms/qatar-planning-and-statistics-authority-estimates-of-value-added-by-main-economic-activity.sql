-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "main_economic_activity_ar",
    "intermediate_goods_services",
    "intermediate_goods_services_services",
    "intermediate_goods_services_goods",
    "production_value",
    "production_value_other_revenues",
    "production_value_products"
FROM "qatar-planning-and-statistics-authority-estimates-of-value-added-by-main-economic-activity"
