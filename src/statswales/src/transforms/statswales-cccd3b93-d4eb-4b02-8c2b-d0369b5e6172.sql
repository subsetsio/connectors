-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Provider Health Board" AS provider_health_board,
    "Date" AS date,
    "Notes" AS notes
FROM "statswales-cccd3b93-d4eb-4b02-8c2b-d0369b5e6172"
