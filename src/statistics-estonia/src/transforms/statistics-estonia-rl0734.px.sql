-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_family",
    "indicator",
    "age_and_number_of_children",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0734.px"
