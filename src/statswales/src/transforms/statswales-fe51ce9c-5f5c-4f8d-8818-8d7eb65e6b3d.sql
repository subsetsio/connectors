-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Level of study" AS level_of_study,
    "Mode of study" AS mode_of_study,
    "Entrant marker" AS entrant_marker,
    "Sex" AS sex,
    "Provider" AS provider,
    "Personal characteristics" AS personal_characteristics,
    "Academic year" AS academic_year,
    "Notes" AS notes
FROM "statswales-fe51ce9c-5f5c-4f8d-8818-8d7eb65e6b3d"
