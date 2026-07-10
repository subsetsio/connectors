-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cnae_2_3_subclasses",
    "descricao",
    "cnae_2",
    "descricao_cnae_2",
    "grupo",
    "descricao_grupo",
    "divisao",
    "descricao_divisao",
    "secao",
    "descricao_secao"
FROM "base-dos-dados-br-bd-diretorios-brasil--cnae-2-3-subclasses"
