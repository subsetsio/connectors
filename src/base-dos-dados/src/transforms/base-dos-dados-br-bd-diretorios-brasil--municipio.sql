-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_municipio",
    "id_municipio_6",
    "id_municipio_tse",
    "id_municipio_rf",
    "id_municipio_bcb",
    "nome",
    "capital_uf",
    "id_comarca",
    "id_regiao_saude",
    "nome_regiao_saude",
    "id_regiao_imediata",
    "nome_regiao_imediata",
    "id_regiao_intermediaria",
    "nome_regiao_intermediaria",
    "id_microrregiao",
    "nome_microrregiao",
    "id_mesorregiao",
    "nome_mesorregiao",
    "id_regiao_metropolitana",
    "nome_regiao_metropolitana",
    "ddd",
    "id_uf",
    "sigla_uf",
    "nome_uf",
    "nome_regiao",
    "amazonia_legal",
    "centroide"
FROM "base-dos-dados-br-bd-diretorios-brasil--municipio"
