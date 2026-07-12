-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "household_size",
    "children_of_different_age",
    "number_of_children_of_different_age",
    "household_composition",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl516.px"
