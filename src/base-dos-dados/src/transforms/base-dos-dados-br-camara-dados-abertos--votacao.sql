-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_votacao",
    strptime("data", '%Y-%m-%d')::DATE AS data,
    strptime("data_registro", '%Y-%m-%d')::DATE AS data_registro,
    "horario_registro",
    "id_orgao",
    "sigla_orgao",
    "id_evento",
    "aprovacao",
    "voto_sim",
    "voto_nao",
    "voto_outro",
    "descricao",
    CAST("data_hora_ultima_votacao" AS TIMESTAMP) AS data_hora_ultima_votacao,
    "descricao_ultima_votacao",
    CAST("data_hora_ultima_proposicao" AS TIMESTAMP) AS data_hora_ultima_proposicao,
    "id_ultima_proposicao",
    "descricao_ultima_proposicao"
FROM "base-dos-dados-br-camara-dados-abertos--votacao"
