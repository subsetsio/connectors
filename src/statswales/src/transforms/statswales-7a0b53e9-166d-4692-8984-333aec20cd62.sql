-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Provider" AS provider,
    "Tenure" AS tenure,
    "Notes" AS notes
FROM "statswales-7a0b53e9-166d-4692-8984-333aec20cd62"
