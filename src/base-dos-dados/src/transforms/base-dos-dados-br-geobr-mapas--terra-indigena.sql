-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_geografico",
    "id_terra_indigena",
    "terra_indigena",
    "etnia",
    "nome_municipio",
    "sigla_uf",
    "area",
    "fase",
    "modalidade",
    "reestudo",
    "indicador_faixa_fronteira",
    "id_unidade_administrativa",
    "sigla_unidade_administrativa",
    "unidade_administrativa",
    "geometria"
FROM "base-dos-dados-br-geobr-mapas--terra-indigena"
