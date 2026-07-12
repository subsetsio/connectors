-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Area" AS area,
    "Provider" AS provider,
    "Dwelling" AS dwelling,
    "Notes" AS notes
FROM "statswales-1cef8d9e-086e-4d90-b3ab-2286bf29f33f"
