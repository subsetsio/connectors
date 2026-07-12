-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Westminster constituency area" AS westminster_constituency_area,
    "Transaction type" AS transaction_type,
    "Notes" AS notes
FROM "statswales-507a2ed8-c368-4763-9032-397e4420a126"
