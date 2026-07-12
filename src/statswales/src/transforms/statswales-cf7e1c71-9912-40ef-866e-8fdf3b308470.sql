-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "School - Sector - Authority" AS school_sector_authority,
    "Notes" AS notes
FROM "statswales-cf7e1c71-9912-40ef-866e-8fdf3b308470"
