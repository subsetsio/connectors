-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Measure" AS measure,
    "Date" AS date,
    "Notes" AS notes
FROM "statswales-d6a0e86a-a6c5-4666-be61-ad491d5b693d"
