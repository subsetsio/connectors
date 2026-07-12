-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "native_and_foreign_origin_population",
    "age_group",
    "place_of_residence",
    "sex",
    "value"
FROM "statistics-estonia-rl0527.px"
