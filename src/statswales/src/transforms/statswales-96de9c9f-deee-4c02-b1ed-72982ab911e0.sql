-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Cause of certification" AS cause_of_certification,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-96de9c9f-deee-4c02-b1ed-72982ab911e0"
