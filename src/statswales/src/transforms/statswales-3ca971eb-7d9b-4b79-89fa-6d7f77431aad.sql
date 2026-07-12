-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Row" AS row,
    "Year" AS year,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-3ca971eb-7d9b-4b79-89fa-6d7f77431aad"
