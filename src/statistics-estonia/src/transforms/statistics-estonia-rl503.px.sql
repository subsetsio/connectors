-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "household_size",
    "age",
    "de_facto_marital_status",
    "place_of_residence",
    "sex",
    "value"
FROM "statistics-estonia-rl503.px"
