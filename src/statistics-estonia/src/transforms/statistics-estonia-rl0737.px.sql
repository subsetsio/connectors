-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_of_man",
    "couples_and_number_of_children_aged_under_18",
    "age_of_woman",
    "county",
    "value"
FROM "statistics-estonia-rl0737.px"
