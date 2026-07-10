-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_regiao_metropolitana",
    "nome",
    "id_recorte_metropolitano",
    "nome_recorte_metropolitano",
    "id_subcategoria_metropolitana",
    "nome_subcategoria_metropolitana",
    "tipo",
    "id_municipio",
    "sigla_uf",
    "nome_regiao"
FROM "base-dos-dados-br-bd-diretorios-brasil--regiao-metropolitana"
