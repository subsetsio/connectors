-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_unidade_conservacao",
    "unidade_conservacao",
    "id_unidade_conservacao_wcmc",
    "id_cnuc",
    "id_geografico",
    "organizacao_orgao",
    "categoria",
    "sigla_grupo",
    "qualidade",
    "esfera",
    "ano_criacao",
    "legislacao",
    strptime("data_ultima", '%Y-%m-%d')::DATE AS data_ultima,
    "geometria"
FROM "base-dos-dados-br-geobr-mapas--unidade-conservacao"
