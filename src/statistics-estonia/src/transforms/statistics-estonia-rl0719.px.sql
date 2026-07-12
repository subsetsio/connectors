-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_members_living_mainly_from_labour_income",
    "indicator",
    "number_of_children_aged_under_18_and_dependants",
    "household_size",
    "county",
    "value"
FROM "statistics-estonia-rl0719.px"
