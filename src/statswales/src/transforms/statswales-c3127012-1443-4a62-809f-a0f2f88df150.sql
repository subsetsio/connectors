-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "School language" AS school_language,
    "Home language" AS home_language,
    "Notes" AS notes
FROM "statswales-c3127012-1443-4a62-809f-a0f2f88df150"
