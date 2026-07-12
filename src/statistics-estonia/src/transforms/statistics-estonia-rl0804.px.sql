-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_and_tenure_status_of_dwelling",
    "sex",
    "persons_status_in_household",
    "age_group",
    "county",
    "value"
FROM "statistics-estonia-rl0804.px"
