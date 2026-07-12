-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Programme type" AS programme_type,
    "Sector" AS sector,
    "Gender" AS gender,
    "Age group" AS age_group,
    "Home region" AS home_region,
    "Quarter" AS quarter,
    "Notes" AS notes
FROM "statswales-3a60fc9b-20ec-4136-be42-00f647ca81f7"
