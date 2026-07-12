-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "place_of_residence_2000",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0552.px"
