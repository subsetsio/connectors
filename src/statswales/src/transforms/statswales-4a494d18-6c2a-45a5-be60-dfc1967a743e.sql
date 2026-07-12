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
    "Disabled status" AS disabled_status,
    "Age" AS age,
    "Notes" AS notes
FROM "statswales-4a494d18-6c2a-45a5-be60-dfc1967a743e"
