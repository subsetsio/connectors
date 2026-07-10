-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "indice_medio",
    "indice",
    "variacao_anual",
    "indice_fechamento_anual"
FROM "base-dos-dados-br-fgv-igp--igp-og-ano"
