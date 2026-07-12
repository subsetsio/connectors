-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Mode of programme" AS mode_of_programme,
    "Provider" AS provider,
    "Standardised activity" AS standardised_activity,
    "Age group" AS age_group,
    "Sector subject area" AS sector_subject_area,
    "Welsh fluency" AS welsh_fluency,
    "Medium of delivery" AS medium_of_delivery,
    "Notes" AS notes
FROM "statswales-f47f34b7-ff58-44a3-a477-f65f2e0163f7"
