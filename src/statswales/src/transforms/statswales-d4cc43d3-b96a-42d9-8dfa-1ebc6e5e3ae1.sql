-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Hospital" AS hospital,
    "Sex" AS sex,
    "Age" AS age,
    "Notes" AS notes
FROM "statswales-d4cc43d3-b96a-42d9-8dfa-1ebc6e5e3ae1"
