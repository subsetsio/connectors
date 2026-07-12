-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Economic status of household" AS economic_status_of_household,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-170d5d46-a9f0-4484-a213-457e2398c816"
