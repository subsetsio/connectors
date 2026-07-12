-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Sector" AS sector,
    "Welsh Medium Type" AS welsh_medium_type,
    "School Language Category" AS school_language_category,
    "Subject" AS subject,
    "Vacancy Medium" AS vacancy_medium,
    "Tenure" AS tenure,
    "Notes" AS notes
FROM "statswales-e983a560-4a49-4173-bb25-df7a76fc42d3"
