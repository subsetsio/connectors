-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Tenure" AS tenure,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-35ace04b-d157-4337-930b-85e29aa66bb9"
