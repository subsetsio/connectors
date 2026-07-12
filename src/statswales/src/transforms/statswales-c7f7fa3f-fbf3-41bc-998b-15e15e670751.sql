-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Geography" AS geography,
    "Sex" AS sex,
    CAST("Year" AS BIGINT) AS year,
    "Notes" AS notes
FROM "statswales-c7f7fa3f-fbf3-41bc-998b-15e15e670751"
