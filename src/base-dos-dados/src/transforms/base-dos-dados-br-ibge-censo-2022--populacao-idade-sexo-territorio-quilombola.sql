-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "territorio_quilombola",
    "sigla_uf",
    "sexo",
    "idade",
    "idade_anos",
    "grupo_idade",
    "populacao_quilombola",
    "populacao"
FROM "base-dos-dados-br-ibge-censo-2022--populacao-idade-sexo-territorio-quilombola"
