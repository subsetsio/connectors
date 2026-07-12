-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "sex",
    "persons_status_in_household",
    "county",
    "legal_marital_status",
    "value"
FROM "statistics-estonia-rl0704.px"
