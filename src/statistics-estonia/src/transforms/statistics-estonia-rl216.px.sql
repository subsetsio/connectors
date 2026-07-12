-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country_of_birth",
    "citizenship",
    "place_of_residence",
    "sex",
    "value"
FROM "statistics-estonia-rl216.px"
