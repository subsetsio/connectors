-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Local health board provider" AS local_health_board_provider,
    "Specialty" AS specialty,
    "Weeks waited" AS weeks_waited,
    "Notes" AS notes
FROM "statswales-abba2e1e-3aff-4df5-8a4c-a1679e4d32e3"
