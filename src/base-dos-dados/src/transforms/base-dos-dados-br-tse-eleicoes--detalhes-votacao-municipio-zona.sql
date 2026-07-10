-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "turno",
    "id_eleicao",
    "tipo_eleicao",
    strptime("data_eleicao", '%Y-%m-%d')::DATE AS data_eleicao,
    "sigla_uf",
    "id_municipio",
    "id_municipio_tse",
    "zona",
    "cargo",
    "aptos",
    "secoes",
    "secoes_agregadas",
    "aptos_totalizadas",
    "secoes_totalizadas",
    "comparecimento",
    "abstencoes",
    "votos_validos",
    "votos_brancos",
    "votos_nulos",
    "votos_nominais",
    "votos_legenda",
    "proporcao_comparecimento",
    "proporcao_votos_validos",
    "proporcao_votos_brancos",
    "proporcao_votos_nulos"
FROM "base-dos-dados-br-tse-eleicoes--detalhes-votacao-municipio-zona"
