-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "id_municipio",
    "nome_municipio",
    "id_uf",
    "sigla_uf",
    "id_regiao",
    "regiao",
    "geometria"
FROM "base-dos-dados-br-geobr-mapas--sede-municipal"
