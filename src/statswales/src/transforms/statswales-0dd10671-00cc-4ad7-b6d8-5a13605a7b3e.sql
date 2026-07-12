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
FROM "statswales-0dd10671-00cc-4ad7-b6d8-5a13605a7b3e"
