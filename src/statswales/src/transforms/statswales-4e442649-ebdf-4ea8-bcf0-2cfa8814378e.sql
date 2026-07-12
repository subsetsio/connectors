-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Geography" AS geography,
    "Sex" AS sex,
    "Age group" AS age_group,
    "Notes" AS notes
FROM "statswales-4e442649-ebdf-4ea8-bcf0-2cfa8814378e"
