-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "id_licitacao",
    "descricao",
    "quantidade_unidade_licitacao",
    "valor_estimado",
    "id_proposta",
    "unidade_proposta",
    "valor_proposta",
    "marca_proposta",
    "cpf_cnpj_fornecedor",
    "fornecedor_situacao",
    strptime("data_proposta", '%Y-%m-%d')::DATE AS data_proposta,
    "validade_proposta"
FROM "base-dos-dados-br-camara-dados-abertos--licitacao-proposta"
