-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "place_of_residence",
    "place_of_residence_2000",
    "value"
FROM "statistics-estonia-rl0558.px"
