-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Age" AS age,
    "Length of time" AS length_of_time,
    "Notes" AS notes
FROM "statswales-2b109ca4-8d27-4046-8531-1ef908793d16"
