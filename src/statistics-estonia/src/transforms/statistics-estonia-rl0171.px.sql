-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "previous_employment",
    "place_of_residence",
    "sex",
    "value"
FROM "statistics-estonia-rl0171.px"
