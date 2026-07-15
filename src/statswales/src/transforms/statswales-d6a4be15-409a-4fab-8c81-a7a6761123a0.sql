-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Service" AS service,
    "Column" AS financial_category,
    "Year" AS year,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-d6a4be15-409a-4fab-8c81-a7a6761123a0"
