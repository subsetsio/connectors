-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Band" AS band,
    "Age" AS age,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-f4888a09-900e-4d3e-91e4-c9ab8def10e1"
