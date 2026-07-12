-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Senedd constituency area" AS senedd_constituency_area,
    "Transaction type" AS transaction_type,
    "Notes" AS notes
FROM "statswales-3a8f9e22-fcf6-451e-b358-a2f6266dcfe5"
