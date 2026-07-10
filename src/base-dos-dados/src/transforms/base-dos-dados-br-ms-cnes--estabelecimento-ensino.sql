-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "sigla_uf",
    "id_municipio",
    "id_estabelecimento_cnes",
    "ano_competencia_inicial",
    "mes_competencia_inicial",
    "ano_competencia_final",
    "mes_competencia_final",
    "tipo_habilitacao",
    "portaria",
    strptime("data_portaria", '%Y-%m-%d')::DATE AS data_portaria,
    "ano_portaria",
    "mes_portaria"
FROM "base-dos-dados-br-ms-cnes--estabelecimento-ensino"
