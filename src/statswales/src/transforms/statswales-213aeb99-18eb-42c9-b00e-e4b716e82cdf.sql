-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Service" AS service,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-213aeb99-18eb-42c9-b00e-e4b716e82cdf"
