-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "id_regiao_metropolitana",
    "sexo",
    "raca_cor",
    "populacao"
FROM "base-dos-dados-br-ibge-pnadc--ano-regiao-metropolitana-raca-cor"
