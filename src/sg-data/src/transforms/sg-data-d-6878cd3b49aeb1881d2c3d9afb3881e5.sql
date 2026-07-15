-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "edu_level",
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
FROM "sg-data-d-6878cd3b49aeb1881d2c3d9afb3881e5"
