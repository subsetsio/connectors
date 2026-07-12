-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Year" AS year,
    "Indicator" AS indicator,
    "Breakdown" AS breakdown,
    "Notes" AS notes
FROM "statswales-491241a0-aaaf-48bb-ad46-4a4ea2e3e792"
