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
    "Marital or civil partnership status" AS marital_or_civil_partnership_status,
    "Notes" AS notes
FROM "statswales-957648bf-6af4-4c52-813c-b9616cb54167"
