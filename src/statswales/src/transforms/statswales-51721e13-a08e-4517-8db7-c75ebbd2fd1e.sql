-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Assessment Type" AS assessment_type,
    "Characteristic or Condition" AS characteristic_or_condition,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-51721e13-a08e-4517-8db7-c75ebbd2fd1e"
