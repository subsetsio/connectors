-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Band" AS band,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-2dbb76bc-8fb3-427d-a46a-445020ab8bc4"
