-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Five equal household groups" AS five_equal_household_groups,
    "Types of expenditure" AS types_of_expenditure,
    "Quarter" AS quarter,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-1900-053v1"
