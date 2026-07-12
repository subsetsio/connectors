-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Local authority area" AS local_authority_area,
    "Transaction type" AS transaction_type,
    "Notes" AS notes
FROM "statswales-01f31768-1255-47be-8233-0f0e31c3d1c8"
