-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Variant" AS variant,
    "Year" AS year,
    "Area" AS area,
    "Sex" AS sex,
    "Age" AS age,
    "Notes" AS notes
FROM "statswales-b9b58daa-967e-496d-82b0-37675fb0534b"
