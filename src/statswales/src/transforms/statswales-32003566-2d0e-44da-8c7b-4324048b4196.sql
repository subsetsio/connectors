-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Welsh port" AS welsh_port,
    "Freight type" AS freight_type,
    "Notes" AS notes
FROM "statswales-32003566-2d0e-44da-8c7b-4324048b4196"
