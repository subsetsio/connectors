-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Provider" AS provider,
    "Mode of study" AS mode_of_study,
    "Level of study" AS level_of_study,
    "Entrant marker" AS entrant_marker,
    "Notes" AS notes
FROM "statswales-fcda7d58-48ac-4cd0-8955-3193446cc2c8"
