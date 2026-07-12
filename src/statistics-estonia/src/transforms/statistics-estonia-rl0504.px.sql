-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ethnic_nationality",
    "sex",
    "country_of_birth",
    "age_group",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0504.px"
