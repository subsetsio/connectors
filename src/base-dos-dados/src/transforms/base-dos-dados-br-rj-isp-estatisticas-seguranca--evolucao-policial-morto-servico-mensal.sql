-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "id_cisp",
    "quantidade_policial_militar_morto_servico",
    "quantidade_policial_civil_morto_servico"
FROM "base-dos-dados-br-rj-isp-estatisticas-seguranca--evolucao-policial-morto-servico-mensal"
