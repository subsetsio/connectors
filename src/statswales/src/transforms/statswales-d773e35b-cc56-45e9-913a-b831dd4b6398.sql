-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Subject" AS subject,
    "Mode of study" AS mode_of_study,
    "Level of study" AS level_of_study,
    "Entrant marker" AS entrant_marker,
    "Country of HE provider" AS country_of_he_provider,
    "Sex" AS sex,
    "Region of permanent address" AS region_of_permanent_address,
    "Notes" AS notes
FROM "statswales-d773e35b-cc56-45e9-913a-b831dd4b6398"
