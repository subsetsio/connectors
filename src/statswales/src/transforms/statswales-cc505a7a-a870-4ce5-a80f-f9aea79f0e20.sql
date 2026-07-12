-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Farm Type" AS farm_type,
    "Cost Heading" AS cost_heading,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-cc505a7a-a870-4ce5-a80f-f9aea79f0e20"
