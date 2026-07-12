-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Authority" AS authority,
    "Row" AS row,
    "Notes" AS notes
FROM "statswales-27b3e04d-fce8-47dc-9e48-7d376c5ef1ca"
