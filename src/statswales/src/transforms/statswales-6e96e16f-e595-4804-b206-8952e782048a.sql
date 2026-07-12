-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Area" AS area,
    "Sex" AS sex,
    "Age" AS age,
    "Notes" AS notes
FROM "statswales-6e96e16f-e595-4804-b206-8952e782048a"
