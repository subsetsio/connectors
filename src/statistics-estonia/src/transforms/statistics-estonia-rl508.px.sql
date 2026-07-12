-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "household_size",
    "number_of_household_members_of_different_age",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl508.px"
