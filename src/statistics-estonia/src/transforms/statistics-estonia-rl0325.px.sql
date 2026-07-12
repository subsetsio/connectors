-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "secondary_place_of_residence",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0325.px"
