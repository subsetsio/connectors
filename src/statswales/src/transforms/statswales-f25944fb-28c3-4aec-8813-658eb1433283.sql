-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Deprivation group" AS deprivation_group,
    "Age group" AS age_group,
    "Sex" AS sex,
    "Disability" AS disability,
    "Notes" AS notes
FROM "statswales-f25944fb-28c3-4aec-8813-658eb1433283"
