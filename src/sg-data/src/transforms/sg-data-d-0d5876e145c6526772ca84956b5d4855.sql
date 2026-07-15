-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "gender",
    "physical_activity",
    "fruit_intake",
    "vegetable_intake",
    "fruit_and_vege_intake",
    "sweetened_drinks_intake",
    "deep_fried_food_intake",
    "salt_use",
    "fat_intake",
    "smoking",
    "binge_drinking"
FROM "sg-data-d-0d5876e145c6526772ca84956b5d4855"
