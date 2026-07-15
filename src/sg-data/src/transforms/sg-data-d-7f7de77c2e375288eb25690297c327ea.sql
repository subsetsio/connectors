-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "types_of_recidivism_rates",
    "2_year_recidivism_rates"
FROM "sg-data-d-7f7de77c2e375288eb25690297c327ea"
