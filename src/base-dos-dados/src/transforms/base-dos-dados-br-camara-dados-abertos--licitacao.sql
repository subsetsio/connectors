-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano_licitacao",
    "id_licitacao",
    "ano_processo",
    "id_processo",
    "objeto",
    "modalidade",
    "tipo",
    "situacao",
    strptime("data_abertura", '%Y-%m-%d')::DATE AS data_abertura,
    strptime("data_publicacao", '%Y-%m-%d')::DATE AS data_publicacao,
    strptime("data_autorizacao", '%Y-%m-%d')::DATE AS data_autorizacao,
    "quantidade_item",
    "quantidade_unidade",
    "quantidade_proposta",
    "quantidade_contrato",
    "valor_estimado",
    "valor_contratado",
    "valor_pago"
FROM "base-dos-dados-br-camara-dados-abertos--licitacao"
