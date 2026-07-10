-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "id_municipio",
    "id_cisp",
    "id_aisp",
    "id_risp",
    "quantidade_arma_fogo_apreendida"
FROM "base-dos-dados-br-rj-isp-estatisticas-seguranca--armas-fogo-apreendidas-mensal"
