-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Local authority" AS local_authority,
    "Age" AS age,
    "Sex" AS sex,
    "Learning centre" AS learning_centre,
    "Notes" AS notes
FROM "statswales-765c5f87-a86d-4c0f-8162-5f7df055cab4"
