-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "parents_country_of_birth",
    "country_of_birth",
    "grandparents_country_of_birth",
    "age_group",
    "county",
    "sex",
    "value"
FROM "statistics-estonia-rl0525.px"
