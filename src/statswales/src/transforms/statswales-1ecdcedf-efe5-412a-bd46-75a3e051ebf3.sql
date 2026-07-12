-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Birth year" AS BIGINT) AS birth_year,
    "Area" AS area,
    "Survival year" AS survival_year,
    "Notes" AS notes
FROM "statswales-1ecdcedf-efe5-412a-bd46-75a3e051ebf3"
