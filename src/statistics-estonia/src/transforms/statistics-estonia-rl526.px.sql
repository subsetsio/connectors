-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_children_and_age_of_youngest_child",
    "age_of_mother_father",
    "family_nucleus_composition_and_employment_of_mother_father",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl526.px"
