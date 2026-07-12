-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Row" AS row,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-4c4b1824-2131-42e2-a125-970098ca0ca1"
