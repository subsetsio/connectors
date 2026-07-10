-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "id_municipio",
    "id_escola",
    "area",
    "localizacao",
    "rede",
    "inse_quantidade_alunos",
    "valor_inse",
    "inse_classificacao_2014",
    "inse_classificacao_2015"
FROM "base-dos-dados-br-inep-indicadores-educacionais--escola-nivel-socioeconomico"
