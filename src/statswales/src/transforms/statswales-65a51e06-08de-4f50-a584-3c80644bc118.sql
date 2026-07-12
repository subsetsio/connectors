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
    "General health" AS general_health,
    "Notes" AS notes
FROM "statswales-65a51e06-08de-4f50-a584-3c80644bc118"
