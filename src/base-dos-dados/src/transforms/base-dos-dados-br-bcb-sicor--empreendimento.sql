-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_empreendimento",
    strptime("data_inicio", '%Y-%m-%d')::DATE AS data_inicio,
    strptime("data_fim", '%Y-%m-%d')::DATE AS data_fim,
    "finalidade",
    "atividade",
    "modalidade",
    "produto",
    "variedade",
    "cesta_safra",
    "zoneamento",
    "unidade_medida",
    "unidade_medida_previsao_producao",
    "consorcio",
    "cedula_mae",
    "id_tipo_cultura"
FROM "base-dos-dados-br-bcb-sicor--empreendimento"
