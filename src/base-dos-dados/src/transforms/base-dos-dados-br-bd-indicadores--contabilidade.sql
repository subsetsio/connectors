-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano_competencia",
    "mes_competencia",
    "ano_caixa",
    "mes_caixa",
    "categoria",
    "tipo",
    "frequencia",
    "equipe",
    "valor"
FROM "base-dos-dados-br-bd-indicadores--contabilidade"
