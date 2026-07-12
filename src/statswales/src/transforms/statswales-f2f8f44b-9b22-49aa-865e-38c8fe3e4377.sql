-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Date" AS BIGINT) AS date,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-f2f8f44b-9b22-49aa-865e-38c8fe3e4377"
