-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Provider Health Board" AS provider_health_board,
    "Data Period Quarter" AS data_period_quarter,
    "Ethnicity" AS ethnicity,
    "Notes" AS notes
FROM "statswales-ff9069e4-ff1e-4fb8-9c5a-8af7d0779999"
