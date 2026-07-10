-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_curso",
    "nome_curso",
    "id_area",
    "nome_area",
    "grau_academico"
FROM "base-dos-dados-br-bd-diretorios-brasil--curso-superior"
