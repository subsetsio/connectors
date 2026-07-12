-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_live_born_children",
    "native_and_foreign_origin_population",
    "age_group",
    "county",
    "value"
FROM "statistics-estonia-rl0534.px"
