-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Provider Health Board" AS provider_health_board,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Notes" AS notes
FROM "statswales-478cd8ba-25d2-4ad0-ad22-c1e33418c586"
