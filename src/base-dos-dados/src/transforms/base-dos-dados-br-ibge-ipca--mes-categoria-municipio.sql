-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "id_municipio",
    "id_categoria",
    "id_categoria_bd",
    "categoria",
    "peso_mensal",
    "variacao_mensal",
    "variacao_anual",
    "variacao_doze_meses"
FROM "base-dos-dados-br-ibge-ipca--mes-categoria-municipio"
