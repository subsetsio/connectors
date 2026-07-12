-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Resident Health Board" AS resident_health_board,
    "Date" AS date,
    "Notes" AS notes
FROM "statswales-e02ee800-dabf-42c6-97a5-5ed215eb0113"
