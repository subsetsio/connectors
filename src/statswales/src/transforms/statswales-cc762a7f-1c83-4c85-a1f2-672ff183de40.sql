-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Fire and Rescue Service" AS fire_and_rescue_service,
    "Notes" AS notes
FROM "statswales-cc762a7f-1c83-4c85-a1f2-672ff183de40"
