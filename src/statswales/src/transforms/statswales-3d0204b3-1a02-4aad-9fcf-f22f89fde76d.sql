-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Farm Type" AS farm_type,
    "Income Type" AS income_type,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-3d0204b3-1a02-4aad-9fcf-f22f89fde76d"
