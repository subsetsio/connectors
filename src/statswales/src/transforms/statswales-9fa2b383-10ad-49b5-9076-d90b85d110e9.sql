-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Sex" AS sex,
    "Subject" AS subject,
    "Notes" AS notes
FROM "statswales-9fa2b383-10ad-49b5-9076-d90b85d110e9"
