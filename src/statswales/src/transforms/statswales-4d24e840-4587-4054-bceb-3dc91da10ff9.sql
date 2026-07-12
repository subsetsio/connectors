-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Provider" AS provider,
    "Country of permanent address" AS country_of_permanent_address,
    "Sex" AS sex,
    "Mode of study" AS mode_of_study,
    "Level of study" AS level_of_study,
    "Entrant marker" AS entrant_marker,
    "Notes" AS notes
FROM "statswales-4d24e840-4587-4054-bceb-3dc91da10ff9"
