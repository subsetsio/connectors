-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_municipio",
    "ano",
    "pib",
    "impostos_liquidos",
    "va",
    "va_agropecuaria",
    "va_industria",
    "va_servicos",
    "va_adespss"
FROM "base-dos-dados-br-ibge-pib--municipio-antigo"
