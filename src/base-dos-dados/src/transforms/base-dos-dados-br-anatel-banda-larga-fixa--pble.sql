-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "dia",
    "sigla_uf",
    "id_municipio",
    "rede",
    "id_escola",
    "empresa",
    "tecnologia",
    "conexao"
FROM "base-dos-dados-br-anatel-banda-larga-fixa--pble"
