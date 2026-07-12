-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Mode of programme" AS mode_of_programme,
    "Home region" AS home_region,
    "Standardised activity" AS standardised_activity,
    "Age group" AS age_group,
    "Activity level" AS activity_level,
    "Welsh fluency" AS welsh_fluency,
    "Medium of delivery" AS medium_of_delivery,
    "Notes" AS notes
FROM "statswales-126fd3f5-a8f4-4a8b-bc14-67b6118f0677"
