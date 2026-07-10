-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cbo_2002",
    "grande_area",
    "descricao_grande_area",
    "atividade",
    "descricao_atividade"
FROM "base-dos-dados-br-ibge-cbo-2002--perfil-ocupacional"
