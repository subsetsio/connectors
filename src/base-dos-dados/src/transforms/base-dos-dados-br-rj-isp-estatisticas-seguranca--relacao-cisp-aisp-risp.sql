-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_risp",
    "id_aisp",
    "id_cisp",
    "id_municipio",
    "unidade_territorial",
    "regiao"
FROM "base-dos-dados-br-rj-isp-estatisticas-seguranca--relacao-cisp-aisp-risp"
