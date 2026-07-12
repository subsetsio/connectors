-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "legal_marital_status",
    "sex",
    "native_and_foreign_origin_population",
    "age_group",
    "county",
    "value"
FROM "statistics-estonia-rl0532.px"
