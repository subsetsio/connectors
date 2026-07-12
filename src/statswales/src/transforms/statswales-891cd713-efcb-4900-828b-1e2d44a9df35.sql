-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Provider" AS provider,
    "Subject" AS subject,
    "Mode of study" AS mode_of_study,
    "Level of study" AS level_of_study,
    "Entrant marker" AS entrant_marker,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-891cd713-efcb-4900-828b-1e2d44a9df35"
