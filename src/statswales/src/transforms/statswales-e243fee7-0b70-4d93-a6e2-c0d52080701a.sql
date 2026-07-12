-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Provider Health Board" AS provider_health_board,
    "Data Period Quarter" AS data_period_quarter,
    "Age" AS age,
    "Gender" AS gender,
    "Notes" AS notes
FROM "statswales-e243fee7-0b70-4d93-a6e2-c0d52080701a"
