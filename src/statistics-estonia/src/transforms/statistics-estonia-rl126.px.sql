-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country_of_birth_and_parents_country_of_birth",
    "ethnic_nationality",
    "place_of_residence",
    "sex",
    "value"
FROM "statistics-estonia-rl126.px"
