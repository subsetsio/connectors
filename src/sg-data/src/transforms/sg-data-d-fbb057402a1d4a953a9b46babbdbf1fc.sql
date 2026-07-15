-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "application_type",
    "no_of_applications"
FROM "sg-data-d-fbb057402a1d4a953a9b46babbdbf1fc"
