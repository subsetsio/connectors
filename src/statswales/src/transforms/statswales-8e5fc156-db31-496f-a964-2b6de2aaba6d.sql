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
    "Disability" AS disability,
    "Notes" AS notes
FROM "statswales-8e5fc156-db31-496f-a964-2b6de2aaba6d"
