-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cbo_2002",
    "descricao",
    "familia",
    "descricao_familia",
    "subgrupo",
    "descricao_subgrupo",
    "subgrupo_principal",
    "descricao_subgrupo_principal",
    "grande_grupo",
    "descricao_grande_grupo"
FROM "base-dos-dados-br-bd-diretorios-brasil--cbo-2002"
