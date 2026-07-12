-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Age" AS age,
    "Sex" AS sex,
    "Geography" AS geography,
    "Notes" AS notes
FROM "statswales-b627861e-a4e6-4299-b389-d44a6ecf6781"
