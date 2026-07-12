-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Sector" AS sector,
    "Welsh Medium Type" AS welsh_medium_type,
    "School Language Category" AS school_language_category,
    "Local Authority" AS local_authority,
    "Sex" AS sex,
    "Staff Category" AS staff_category,
    "Notes" AS notes
FROM "statswales-8dd51737-a08b-430b-ae0e-84e5171352b4"
