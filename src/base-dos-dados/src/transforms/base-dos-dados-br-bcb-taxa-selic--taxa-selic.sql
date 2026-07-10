-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("data", '%Y-%m-%d')::DATE AS data,
    "valor"
FROM "base-dos-dados-br-bcb-taxa-selic--taxa-selic"
