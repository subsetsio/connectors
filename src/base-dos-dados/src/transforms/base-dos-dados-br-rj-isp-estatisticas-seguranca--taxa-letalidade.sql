-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "regiao",
    "delito",
    "contagem_delito",
    "populacao",
    "taxa_cem_mil_habitantes"
FROM "base-dos-dados-br-rj-isp-estatisticas-seguranca--taxa-letalidade"
