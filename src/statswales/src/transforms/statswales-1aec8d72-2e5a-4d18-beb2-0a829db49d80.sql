-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Area of work" AS area_of_work,
    "Job type" AS job_type,
    "Organisation" AS organisation,
    "Notes" AS notes
FROM "statswales-1aec8d72-2e5a-4d18-beb2-0a829db49d80"
