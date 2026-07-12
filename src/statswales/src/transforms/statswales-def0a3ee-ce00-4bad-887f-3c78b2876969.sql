-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Local health board" AS local_health_board,
    "Local authority of residence" AS local_authority_of_residence,
    "Reason for delay" AS reason_for_delay,
    "Date" AS date,
    "Notes" AS notes
FROM "statswales-def0a3ee-ce00-4bad-887f-3c78b2876969"
