-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Local health board provider" AS local_health_board_provider,
    "Service" AS service,
    "Notes" AS notes
FROM "statswales-f40980fd-05bc-4e8a-9576-21021be38913"
