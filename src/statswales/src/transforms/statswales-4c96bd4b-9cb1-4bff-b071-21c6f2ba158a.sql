-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data values" AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Fire and Rescue Service" AS fire_and_rescue_service,
    "Notes" AS notes
FROM "statswales-4c96bd4b-9cb1-4bff-b071-21c6f2ba158a"
