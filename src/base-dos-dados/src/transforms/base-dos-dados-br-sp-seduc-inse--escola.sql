-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_municipio",
    "rede",
    "diretoria",
    "id_escola",
    "id_escola_sp",
    "nivel_socio_economico"
FROM "base-dos-dados-br-sp-seduc-inse--escola"
