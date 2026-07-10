-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_uf",
    "sigla_uf",
    "id_municipio",
    "nome_municipio",
    "id_distrito",
    "nome_distrito",
    "id_subdistrito",
    "nome_subdistrito",
    "id_vizinhanca",
    "nome_vizinhanca",
    "referencia_geometria",
    "geometria"
FROM "base-dos-dados-br-geobr-mapas--limite-vizinhanca"
