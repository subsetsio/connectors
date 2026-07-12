-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Outcome" AS outcome,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-38a0c155-8408-4681-af24-2755b4d22287"
