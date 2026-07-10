-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "sigla_uf",
    "tipo_consumo",
    "numero_consumidores",
    "consumo"
FROM "base-dos-dados-br-mme-consumo-energia-eletrica--uf"
