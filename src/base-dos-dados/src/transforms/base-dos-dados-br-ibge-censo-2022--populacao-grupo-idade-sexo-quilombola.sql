-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "id_municipio",
    "localizacao_domicilio",
    "grupo_idade",
    "sexo",
    "populacao_quilombola"
FROM "base-dos-dados-br-ibge-censo-2022--populacao-grupo-idade-sexo-quilombola"
