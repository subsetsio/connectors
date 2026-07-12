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
FROM "statswales-32f4b9c8-b5c7-460b-bc0c-00ed8adbc6de"
