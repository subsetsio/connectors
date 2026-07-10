-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "sigla_uf",
    "id_municipio",
    "emissao_co2",
    "emissao_mp"
FROM "base-dos-dados-br-mobilidados-indicadores--emissao-co2-material-particulado"
