-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Application workstage" AS application_workstage,
    "Month" AS month,
    "Academic year" AS academic_year,
    "Notes" AS notes
FROM "statswales-a5a1d52c-1146-48f4-a8f1-13677d5863e7"
