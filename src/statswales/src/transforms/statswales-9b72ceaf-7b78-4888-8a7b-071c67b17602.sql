-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Age" AS age,
    "Sector" AS sector,
    "Gender" AS gender,
    "Mode" AS mode,
    "Notes" AS notes
FROM "statswales-9b72ceaf-7b78-4888-8a7b-071c67b17602"
