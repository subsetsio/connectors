-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data values" AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Fire and Rescue Service" AS fire_and_rescue_service,
    "Completions" AS completions,
    "Notes" AS notes
FROM "statswales-bee66abf-b0a1-4f0f-8d41-187e1c8dc9f9"
