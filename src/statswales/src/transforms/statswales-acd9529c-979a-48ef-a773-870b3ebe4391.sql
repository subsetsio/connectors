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
    "Notes" AS notes
FROM "statswales-acd9529c-979a-48ef-a773-870b3ebe4391"
