-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "subclasse",
    "descricao_subclasse",
    "classe",
    "descricao_classe",
    "grupo",
    "descricao_grupo",
    "divisao",
    "descricao_divisao",
    "secao",
    "descricao_secao",
    "indicador_cnae_2_0",
    "indicador_cnae_2_1",
    "indicador_cnae_2_2",
    "indicador_cnae_2_3"
FROM "base-dos-dados-br-bd-diretorios-brasil--cnae-2"
