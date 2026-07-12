-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "persons_status_in_household",
    "sex",
    "age_group",
    "socio_economic_status",
    "county",
    "value"
FROM "statistics-estonia-rl0705.px"
