-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Size band" AS size_band,
    "Ownership" AS ownership,
    "Variable" AS variable,
    "Notes" AS notes
FROM "statswales-5247d9fa-fcc3-4c75-ab27-a4eda0859927"
