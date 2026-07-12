-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Local Health Board" AS local_health_board,
    "Quarter" AS quarter,
    "Milk type" AS milk_type,
    "Age of baby" AS age_of_baby,
    "Notes" AS notes
FROM "statswales-763d4890-8984-49fe-a6fc-1ac46ca0f889"
