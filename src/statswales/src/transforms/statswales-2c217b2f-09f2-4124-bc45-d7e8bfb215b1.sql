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
FROM "statswales-2c217b2f-09f2-4124-bc45-d7e8bfb215b1"
