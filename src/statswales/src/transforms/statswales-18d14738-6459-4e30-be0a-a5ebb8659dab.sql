-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Band" AS band,
    "Measure" AS measure,
    "Date" AS date,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-18d14738-6459-4e30-be0a-a5ebb8659dab"
