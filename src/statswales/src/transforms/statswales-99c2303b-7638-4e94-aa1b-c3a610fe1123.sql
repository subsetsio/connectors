-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Mode" AS mode,
    "Type of Practitioner" AS type_of_practitioner,
    "Reason" AS reason,
    "Date" AS date,
    "Notes" AS notes
FROM "statswales-99c2303b-7638-4e94-aa1b-c3a610fe1123"
