-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "command_of_foreign_languages",
    "educational_attainment",
    "age_group",
    "county",
    "sex",
    "value"
FROM "statistics-estonia-rl0441.px"
