-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "children_and_the_age_of_youngest_child",
    "partner",
    "age",
    "economic_activity",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl518.px"
