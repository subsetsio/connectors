-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Sector" AS sector,
    "Welsh Medium Type" AS welsh_medium_type,
    "School Language Category" AS school_language_category,
    "Tenure" AS tenure,
    "Absence Type" AS absence_type,
    "Month" AS month,
    "Notes" AS notes
FROM "statswales-cffa53ad-4afe-4f59-9bb9-ea67a17ecf9a"
