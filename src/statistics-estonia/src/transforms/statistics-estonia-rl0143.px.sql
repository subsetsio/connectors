-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "sex",
    "main_source_of_subsistence",
    "county",
    "ethnic_nationality",
    "value"
FROM "statistics-estonia-rl0143.px"
