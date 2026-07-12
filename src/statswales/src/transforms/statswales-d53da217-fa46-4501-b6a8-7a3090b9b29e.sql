-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Measure" AS measure,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-d53da217-fa46-4501-b6a8-7a3090b9b29e"
