-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Sector" AS sector,
    "Sex" AS sex,
    "Welsh Medium Type" AS welsh_medium_type,
    "School Language Category" AS school_language_category,
    "National Identity" AS national_identity,
    "Notes" AS notes
FROM "statswales-61a04b39-273f-4b5f-b72f-d17466de0d22"
