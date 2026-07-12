-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Row" AS row,
    "Band" AS band,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-062488e2-3fd6-4755-9b0b-a64547fc570f"
