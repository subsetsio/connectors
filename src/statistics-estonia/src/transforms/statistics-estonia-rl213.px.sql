-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_children_given_birth_to",
    "age_at_the_time_of_birth_of_the_first_child",
    "ethnic_nationality_of_woman",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl213.px"
