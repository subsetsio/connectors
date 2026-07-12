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
    "Sex" AS sex,
    "Age Range" AS age_range,
    "Staff Category" AS staff_category,
    "Notes" AS notes
FROM "statswales-feb9b641-eb90-41e4-abc7-31de8898799e"
