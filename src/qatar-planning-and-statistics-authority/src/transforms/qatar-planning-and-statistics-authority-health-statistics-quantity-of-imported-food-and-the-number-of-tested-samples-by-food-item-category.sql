-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "food_item_category",
    "food_item_category_ar",
    "usable_quantity_kg",
    "rejected_quantity_kg",
    "returned_quantity_kg",
    "disposed_quantity_kg",
    "undamaged_samples",
    "damaged_samples"
FROM "qatar-planning-and-statistics-authority-health-statistics-quantity-of-imported-food-and-the-number-of-tested-samples-by-food-item-category"
