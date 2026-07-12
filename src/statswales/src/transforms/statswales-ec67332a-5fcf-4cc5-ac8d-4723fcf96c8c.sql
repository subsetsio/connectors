-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Age" AS age,
    "Symptoms" AS symptoms,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-ec67332a-5fcf-4cc5-ac8d-4723fcf96c8c"
