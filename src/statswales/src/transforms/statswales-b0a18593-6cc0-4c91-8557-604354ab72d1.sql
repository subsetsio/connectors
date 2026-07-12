-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Built-up area" AS built_up_area,
    "Transaction type" AS transaction_type,
    "Notes" AS notes
FROM "statswales-b0a18593-6cc0-4c91-8557-604354ab72d1"
