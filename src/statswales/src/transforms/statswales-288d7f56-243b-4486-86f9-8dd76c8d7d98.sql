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
FROM "statswales-288d7f56-243b-4486-86f9-8dd76c8d7d98"
