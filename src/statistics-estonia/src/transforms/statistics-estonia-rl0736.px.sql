-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_of_man",
    "type_of_family",
    "number_of_children_and_age_of_youngest_child",
    "county",
    "indicator",
    "value"
FROM "statistics-estonia-rl0736.px"
