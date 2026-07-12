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
    "Religion" AS religion,
    "Notes" AS notes
FROM "statswales-2a78f6af-1956-4384-9e71-31291641dbf0"
