-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Service" AS service,
    "Area" AS area,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-cf127c8e-4469-4636-a40d-c343b3df3b26"
