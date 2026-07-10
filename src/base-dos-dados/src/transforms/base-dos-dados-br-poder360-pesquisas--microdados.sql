-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_pesquisa",
    "ano",
    "sigla_uf",
    "nome_municipio",
    "cargo",
    strptime("data", '%Y-%m-%d')::DATE AS data,
    "data_referencia",
    "instituto",
    "contratante",
    "orgao_registro",
    "numero_registro",
    "quantidade_entrevistas",
    "margem_mais",
    "margem_menos",
    "tipo",
    "turno",
    "tipo_voto",
    "id_cenario",
    "descricao_cenario",
    "id_candidato_poder360",
    "nome_candidato",
    "sigla_partido",
    "condicao",
    "percentual"
FROM "base-dos-dados-br-poder360-pesquisas--microdados"
