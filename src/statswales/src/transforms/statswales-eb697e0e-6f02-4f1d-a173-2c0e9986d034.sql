-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "School" AS school,
    "Sector" AS sector,
    "Component" AS component,
    "Notes" AS notes
FROM "statswales-eb697e0e-6f02-4f1d-a173-2c0e9986d034"
