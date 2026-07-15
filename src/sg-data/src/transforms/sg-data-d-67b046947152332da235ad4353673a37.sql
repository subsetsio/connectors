-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "highest_qualification",
    "age",
    "outside_labour_force"
FROM "sg-data-d-67b046947152332da235ad4353673a37"
