-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano_licitacao",
    "id_licitacao",
    "tipo_registo",
    "ano_pedido",
    "id_pedido",
    strptime("data_cadastro", '%Y-%m-%d')::DATE AS data_cadastro,
    "horario_cadastro",
    "id_orgao",
    "orgao",
    "descricao",
    "observacao"
FROM "base-dos-dados-br-camara-dados-abertos--licitacao-pedido"
