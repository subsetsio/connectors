-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_pais_m49",
    "id_pais_fao",
    "id_pais_gaul",
    "sigla_pais_iso3",
    "sigla_pais_iso2",
    "sigla_pais_pnud",
    "sigla_pais_coi",
    "sigla_pais_fifa",
    "nome",
    "nome_ingles",
    "nome_oficial_ingles",
    "nacionalidade",
    "sigla_continente"
FROM "base-dos-dados-br-bd-diretorios-mundo--pais"
