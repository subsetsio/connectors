-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Number of Welsh medium credits" AS number_of_welsh_medium_credits,
    "Provider" AS provider,
    "Mode of study" AS mode_of_study,
    "Level of study" AS level_of_study,
    "Domicile" AS domicile,
    "Welsh speaking ability" AS welsh_speaking_ability,
    "Sex" AS sex,
    "Entrant marker" AS entrant_marker,
    "Notes" AS notes
FROM "statswales-3e4b0e1b-5da9-4b8c-8797-9dd08cd6e176"
