-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_orgao",
    "nome",
    "apelido",
    "sigla",
    "tipo_orgao",
    strptime("data_inicio", '%Y-%m-%d')::DATE AS data_inicio,
    strptime("data_instalacao", '%Y-%m-%d')::DATE AS data_instalacao,
    strptime("data_final", '%Y-%m-%d')::DATE AS data_final,
    "situacao",
    "casa",
    "sala"
FROM "base-dos-dados-br-camara-dados-abertos--orgao"
