-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Transaction type" AS transaction_type,
    "Transaction description" AS transaction_description,
    "Notes" AS notes
FROM "statswales-bed56fe8-0d85-4c80-bddc-9a873bcc599f"
