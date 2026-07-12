-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "citizenship",
    "sex",
    "place_of_residence",
    "age_group",
    "value"
FROM "statistics-estonia-rl0422.px"
