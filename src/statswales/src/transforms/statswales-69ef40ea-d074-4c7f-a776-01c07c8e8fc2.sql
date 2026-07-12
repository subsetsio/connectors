-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Survey year" AS survey_year,
    "Region" AS region,
    "Notes" AS notes
FROM "statswales-69ef40ea-d074-4c7f-a776-01c07c8e8fc2"
