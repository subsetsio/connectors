-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Deprivation area" AS deprivation_area,
    "Transaction type" AS transaction_type,
    "Notes" AS notes
FROM "statswales-b5c05751-d773-46ea-a1af-5a9e1c6df46a"
