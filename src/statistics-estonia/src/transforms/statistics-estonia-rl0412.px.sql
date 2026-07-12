-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group_of_woman",
    "number_of_live_born_children",
    "place_of_residence_of_woman",
    "value"
FROM "statistics-estonia-rl0412.px"
