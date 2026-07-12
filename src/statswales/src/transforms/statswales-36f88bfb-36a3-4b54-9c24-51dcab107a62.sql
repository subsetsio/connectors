-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Pollutant" AS pollutant,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-36f88bfb-36a3-4b54-9c24-51dcab107a62"
