-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local authority" AS local_authority,
    "Category" AS category,
    "Notes" AS notes
FROM "statswales-7be88416-50db-4a08-917d-ca6e4a17db39"
