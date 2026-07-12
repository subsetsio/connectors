-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Geography" AS geography,
    "Sex" AS sex,
    "Age" AS age,
    "Notes" AS notes
FROM "statswales-3a324dc0-3594-447f-9b4a-1a08bb923bf8"
