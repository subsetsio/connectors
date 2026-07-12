-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_rooms_per_inhabitant",
    "age_and_number_of_children",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0826.px"
