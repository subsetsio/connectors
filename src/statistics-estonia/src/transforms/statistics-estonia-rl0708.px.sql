-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "household_size",
    "de_facto_marital_status",
    "age_group",
    "legal_marital_status",
    "county",
    "sex",
    "value"
FROM "statistics-estonia-rl0708.px"
