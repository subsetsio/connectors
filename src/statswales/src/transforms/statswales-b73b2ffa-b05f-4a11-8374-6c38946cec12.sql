-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Ethnicity" AS ethnicity,
    "Subject" AS subject,
    "Notes" AS notes
FROM "statswales-b73b2ffa-b05f-4a11-8374-6c38946cec12"
