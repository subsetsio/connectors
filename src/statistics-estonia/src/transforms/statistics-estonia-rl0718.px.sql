-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "socio_economic_status_number_of_working_and_unemployed_members",
    "household_structure",
    "county",
    "indicator",
    "value"
FROM "statistics-estonia-rl0718.px"
