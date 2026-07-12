-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Description" AS description,
    "Transaction type" AS transaction_type,
    "Notes" AS notes
FROM "statswales-60a57730-166f-486d-9315-69f7fd4c78b1"
