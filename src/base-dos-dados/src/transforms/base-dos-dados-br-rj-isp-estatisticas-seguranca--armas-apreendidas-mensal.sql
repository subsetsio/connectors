-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "id_cisp",
    "id_aisp",
    "id_risp",
    "quantidade_arma_fabricacao_caseira",
    "quantidade_carabina",
    "quantidade_espingarda",
    "quantidade_fuzil",
    "quantidade_garrucha",
    "quantidade_garruchao",
    "quantidade_metralhadora",
    "quantidade_outros",
    "quantidade_pistola",
    "quantidade_revolver",
    "quantidade_submetralhadora",
    "total"
FROM "base-dos-dados-br-rj-isp-estatisticas-seguranca--armas-apreendidas-mensal"
