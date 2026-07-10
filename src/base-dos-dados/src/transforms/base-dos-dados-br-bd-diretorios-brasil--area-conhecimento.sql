-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "especialidade",
    "descricao_especialidade",
    "subarea",
    "descricao_subarea",
    "area",
    "descricao_area",
    "grande_area",
    "descricao_grande_area"
FROM "base-dos-dados-br-bd-diretorios-brasil--area-conhecimento"
