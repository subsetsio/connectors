-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Area" AS area,
    "Age" AS age,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-e8863ec1-2e01-4a04-9a4b-b73b32233d0d"
