-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Row" AS row,
    "Column" AS financial_category,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-475612f0-9e2f-4966-9fcd-b790b5a81b1f"
