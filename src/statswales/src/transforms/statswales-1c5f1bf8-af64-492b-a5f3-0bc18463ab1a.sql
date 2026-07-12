-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Subject" AS subject,
    "Sex" AS sex,
    "Assessment type" AS assessment_type,
    "Notes" AS notes
FROM "statswales-1c5f1bf8-af64-492b-a5f3-0bc18463ab1a"
