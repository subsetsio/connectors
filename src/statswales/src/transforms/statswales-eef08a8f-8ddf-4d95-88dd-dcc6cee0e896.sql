-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Application outcome" AS application_outcome,
    "Mode of study" AS mode_of_study,
    "Income band" AS income_band,
    "Local authority (student)" AS local_authority_student,
    "Institution type" AS institution_type,
    "Notes" AS notes
FROM "statswales-eef08a8f-8ddf-4d95-88dd-dcc6cee0e896"
