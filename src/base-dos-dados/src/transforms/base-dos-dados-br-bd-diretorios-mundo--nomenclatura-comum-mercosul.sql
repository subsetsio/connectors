-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_ncm",
    "id_unidade",
    "id_sh6",
    "id_ppe",
    "id_ppi",
    "id_fator_agregado_ncm",
    "id_cgce_n3",
    "id_isic_classe",
    "id_siit",
    "id_cuci_item",
    "nome_unidade",
    "nome_ncm_portugues",
    "nome_ncm_espanhol",
    "nome_ncm_ingles"
FROM "base-dos-dados-br-bd-diretorios-mundo--nomenclatura-comum-mercosul"
