-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age",
    "ethnic_nationality",
    "number_of_inhabitants",
    "number_of_rooms",
    "place_of_residence",
    "sex",
    "value"
FROM "statistics-estonia-rl803.px"
