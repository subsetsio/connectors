-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Economic status of household" AS economic_status_of_household,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-b7d80bf8-9d8c-4e84-9761-e39b03905557"
