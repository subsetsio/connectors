-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "numero_indice",
    "variacao_mensal",
    "variacao_anual",
    "variacao_doze_meses"
FROM "base-dos-dados-br-ibge-ipp--mes-industria-extrativa"
