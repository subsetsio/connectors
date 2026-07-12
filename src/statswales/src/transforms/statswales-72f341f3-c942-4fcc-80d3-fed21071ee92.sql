-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Industry" AS industry,
    "Size band" AS size_band,
    "Variable" AS variable,
    "Notes" AS notes
FROM "statswales-72f341f3-c942-4fcc-80d3-fed21071ee92"
