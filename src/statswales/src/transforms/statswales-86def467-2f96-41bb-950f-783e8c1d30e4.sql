-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Band" AS band,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-86def467-2f96-41bb-950f-783e8c1d30e4"
