-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_terra_indigena",
    "terra_indigena",
    "sigla_uf",
    "domicilios",
    "populacao",
    "populacao_indigena"
FROM "base-dos-dados-br-ibge-censo-2022--terra-indigena"
