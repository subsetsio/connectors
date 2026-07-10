-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("data", '%Y-%m-%d')::DATE AS data,
    "subsistema",
    "energia_armazenada_maxima",
    "energia_armazenada_verificada",
    "proporcao_energia_armazenada_verificada"
FROM "base-dos-dados-br-ons-energia-armazenada--subsistemas"
