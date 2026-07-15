-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "elderly_pop",
    "sex",
    "marital_status",
    "percentage"
FROM "sg-data-d-76eb0a0d52db203284c50ccfba84c815"
