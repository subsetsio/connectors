-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Characteristic or Condition" AS characteristic_or_condition,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-7b051cd5-b269-4e58-9647-f7c6cb88369f"
