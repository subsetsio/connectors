-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_arranjo_populacional",
    "arranjo_populacional",
    "populacao_urbana_2010",
    "populacao_rural_2010",
    "populacao_2010",
    "id_municipio",
    "sigla_uf",
    "geometria"
FROM "base-dos-dados-br-geobr-mapas--arranjo-populacional"
