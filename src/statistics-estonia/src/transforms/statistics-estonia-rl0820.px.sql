-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "comfort_characteristics",
    "type_of_building",
    "household_structure",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0820.px"
