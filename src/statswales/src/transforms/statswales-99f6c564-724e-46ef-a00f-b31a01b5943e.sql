-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Sector" AS sector,
    "Local Authority" AS local_authority,
    "Staff Category" AS staff_category,
    "Welsh Ability" AS welsh_ability,
    "Welsh Medium Type" AS welsh_medium_type,
    "School Language Category" AS school_language_category,
    "Notes" AS notes
FROM "statswales-99f6c564-724e-46ef-a00f-b31a01b5943e"
