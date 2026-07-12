-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Farm Type" AS farm_type,
    "Output Type" AS output_type,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-e38b0187-c261-41f8-8803-b9fee7ac3fe8"
