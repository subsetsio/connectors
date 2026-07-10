-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "cisp",
    "pm_mortos_serviso",
    "pc_mortos_servicos"
FROM "base-dos-dados-br-isp-estatisticas-seguranca--policiais-mortos-servico"
