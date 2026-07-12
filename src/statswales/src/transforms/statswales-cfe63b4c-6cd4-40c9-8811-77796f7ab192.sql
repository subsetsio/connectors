-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Geography" AS geography,
    "Age" AS age,
    "Ethnicity" AS ethnicity,
    "Notes" AS notes
FROM "statswales-cfe63b4c-6cd4-40c9-8811-77796f7ab192"
