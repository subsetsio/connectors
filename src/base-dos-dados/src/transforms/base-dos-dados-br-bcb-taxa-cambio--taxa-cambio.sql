-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    strptime("data_cotacao", '%Y-%m-%d')::DATE AS data_cotacao,
    "hora_cotacao",
    "moeda",
    "tipo_moeda",
    "tipo_boletim",
    "paridade_compra",
    "paridade_venda",
    "cotacao_compra",
    "cotacao_venda"
FROM "base-dos-dados-br-bcb-taxa-cambio--taxa-cambio"
