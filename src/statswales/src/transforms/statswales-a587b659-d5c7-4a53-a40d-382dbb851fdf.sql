-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Row description" AS row_description,
    "Local authority" AS local_authority,
    "Notes" AS notes
FROM "statswales-a587b659-d5c7-4a53-a40d-382dbb851fdf"
