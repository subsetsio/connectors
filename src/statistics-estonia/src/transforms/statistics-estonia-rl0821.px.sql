-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "comfort_characteristics",
    "age_and_number_of_children",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0821.px"
