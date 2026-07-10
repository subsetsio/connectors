-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "nome",
    "nome_pais",
    "sigla_uf",
    "nome_municipio_origem",
    "genero",
    "ocupacao",
    "instituicao",
    "categoria",
    "indicador_juri_intermediario",
    "indicador_juri_final"
FROM "base-dos-dados-world-oceanos-mapeamento--historico-jurados"
