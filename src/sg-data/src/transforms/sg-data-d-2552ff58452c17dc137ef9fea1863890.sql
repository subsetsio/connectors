-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "types_of_recidivism_rates",
    "5_year_recidivism_rates"
FROM "sg-data-d-2552ff58452c17dc137ef9fea1863890"
