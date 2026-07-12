-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Local Health Board" AS local_health_board,
    "Quarter" AS quarter,
    "Milk type" AS milk_type,
    "Age of baby" AS age_of_baby,
    "Notes" AS notes
FROM "statswales-3ca7a492-8256-4e2e-a926-3863c49d4972"
