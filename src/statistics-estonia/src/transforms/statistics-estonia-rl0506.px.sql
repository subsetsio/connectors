-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "educational_attainment",
    "ethnic_nationality",
    "sex",
    "country_of_birth",
    "age_group",
    "county",
    "citizenship",
    "value"
FROM "statistics-estonia-rl0506.px"
