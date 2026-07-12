-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Item" AS item,
    strptime("Year", '%d/%m/%Y')::DATE AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-f5df167d-d979-4647-87ac-5d1ba5c9f437"
