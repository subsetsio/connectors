-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Provider Health Board" AS provider_health_board,
    "Data Period Quarter" AS data_period_quarter,
    "Assessment Outcome" AS assessment_outcome,
    "Notes" AS notes
FROM "statswales-e943659b-68d5-493b-8da3-e2458599ed14"
