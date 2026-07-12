-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Programme type" AS programme_type,
    "Gender" AS gender,
    "Age group" AS age_group,
    "Ethnic background" AS ethnic_background,
    "Home region" AS home_region,
    "Quarter" AS quarter,
    "Notes" AS notes
FROM "statswales-781ddf6a-6765-4264-8a60-657ef9cc278c"
