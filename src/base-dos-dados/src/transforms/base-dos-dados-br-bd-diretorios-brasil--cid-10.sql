-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "subcategoria",
    "descricao_subcategoria",
    "categoria",
    "descricao_categoria",
    "capitulo",
    "descricao_capitulo",
    "causa_violencia",
    "causa_overdose"
FROM "base-dos-dados-br-bd-diretorios-brasil--cid-10"
