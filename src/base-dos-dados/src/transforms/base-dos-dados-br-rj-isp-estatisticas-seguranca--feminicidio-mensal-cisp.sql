-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "id_cisp",
    "quantidade_morte_feminicidio",
    "quantidade_tentativa_feminicidio",
    "tipo_fase"
FROM "base-dos-dados-br-rj-isp-estatisticas-seguranca--feminicidio-mensal-cisp"
