-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "indice",
    "variacao_mensal",
    "variacao_12_meses",
    "variacao_acumulada_ano",
    "indice_fechamento_mensal"
FROM "base-dos-dados-br-fgv-igp--igp-di-mes"
