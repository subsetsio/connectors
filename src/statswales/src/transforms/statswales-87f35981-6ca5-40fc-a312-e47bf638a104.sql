-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Transaction value" AS transaction_value,
    "Transaction type" AS transaction_type,
    "Notes" AS notes
FROM "statswales-87f35981-6ca5-40fc-a312-e47bf638a104"
