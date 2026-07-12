-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Fire and rescue service area" AS fire_and_rescue_service_area,
    "Notes" AS notes
FROM "statswales-d5ad27d2-15e2-4e8e-a060-831dd7fa2a48"
