-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Local health board provider" AS local_health_board_provider,
    "Local health board of residence" AS local_health_board_of_residence,
    "Source of referral" AS source_of_referral,
    "Specialty" AS specialty,
    "Notes" AS notes
FROM "statswales-9e8f6f1d-d4aa-457a-a675-cc0e2caef3a5"
