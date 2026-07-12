-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Prescribers" AS prescribers,
    "Year" AS year,
    "Type of Prescriber" AS type_of_prescriber,
    "Notes" AS notes
FROM "statswales-47bd3a34-5f14-4ee3-98d6-3f4f0a996aca"
