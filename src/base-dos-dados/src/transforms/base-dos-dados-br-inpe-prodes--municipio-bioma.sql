-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "id_municipio",
    "bioma",
    "area_total",
    "desmatado",
    "vegetacao_natural",
    "nao_vegetacao_natural",
    "hidrografia"
FROM "base-dos-dados-br-inpe-prodes--municipio-bioma"
