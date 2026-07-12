-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Farm Size" AS farm_size,
    "Income Type" AS income_type,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-2553069e-02e7-4763-972a-54d8c4a7ebbc"
