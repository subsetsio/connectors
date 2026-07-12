-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_at_the_birth_of_the_first_child",
    "number_of_live_born_children",
    "age_group_of_woman",
    "county",
    "ethnic_nationality_of_woman",
    "value"
FROM "statistics-estonia-rl0419.px"
