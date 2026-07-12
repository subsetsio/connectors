-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Tenure" AS tenure,
    "Time period" AS time_period,
    "Migrant status of the head of household" AS migrant_status_of_the_head_of_household,
    "Notes" AS notes
FROM "statswales-4d82a2e7-9284-41f1-b0d7-fea06d2e71fa"
