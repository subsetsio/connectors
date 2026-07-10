-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nome",
    "cargo",
    "funcao",
    strptime("data_inicio_historico", '%Y-%m-%d')::DATE AS data_inicio_historico,
    strptime("data_nomeacao", '%Y-%m-%d')::DATE AS data_nomeacao,
    strptime("data_publicacao_nomeacao", '%Y-%m-%d')::DATE AS data_publicacao_nomeacao,
    "grupo",
    "ponto",
    "ato_nomeacao",
    "lotacao"
FROM "base-dos-dados-br-camara-dados-abertos--funcionario"
