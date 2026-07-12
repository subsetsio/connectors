-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data values" AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Fire and Rescue Service" AS fire_and_rescue_service,
    "Premise Type" AS premise_type,
    "Notes" AS notes
FROM "statswales-92e950e4-00d6-43c9-9f59-e84b41fdeb05"
