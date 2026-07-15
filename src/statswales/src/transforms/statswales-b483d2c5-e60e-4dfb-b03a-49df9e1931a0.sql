-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Service" AS service,
    "Column" AS financial_category,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-b483d2c5-e60e-4dfb-b03a-49df9e1931a0"
