-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Deprivation group" AS deprivation_group,
    "Welsh language skills" AS welsh_language_skills,
    "Notes" AS notes
FROM "statswales-3091a6ef-3ad4-43f0-acf6-e1ebb89e68ec"
