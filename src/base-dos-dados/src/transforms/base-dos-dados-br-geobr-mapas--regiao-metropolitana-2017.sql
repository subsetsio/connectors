-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nome_regiao_metropolitana",
    "tipo",
    "subcategoria_metropolitana",
    "id_municipio",
    "sigla_uf",
    "legislacao",
    strptime("data_legislacao", '%Y-%m-%d')::DATE AS data_legislacao,
    "geometria"
FROM "base-dos-dados-br-geobr-mapas--regiao-metropolitana-2017"
