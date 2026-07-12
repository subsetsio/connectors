-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Area" AS area,
    "Household Type" AS household_type,
    "Notes" AS notes
FROM "statswales-ce1308bb-9afd-4107-ae5a-38d3022c7181"
