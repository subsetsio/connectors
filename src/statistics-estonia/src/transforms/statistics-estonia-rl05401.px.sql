-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_generations_in_household",
    "sex",
    "native_and_foreign_origin_population",
    "age_group",
    "county",
    "value"
FROM "statistics-estonia-rl05401.px"
