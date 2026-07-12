-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Area" AS area,
    "Age" AS age,
    "Gender" AS gender,
    "Notes" AS notes
FROM "statswales-86c2d09d-d229-4598-b585-17584c7daca2"
