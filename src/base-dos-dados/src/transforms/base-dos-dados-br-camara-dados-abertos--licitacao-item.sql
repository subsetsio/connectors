-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano_licitacao",
    "id_licitacao",
    "id_item",
    "id_sub_item",
    "descricao",
    "especificacao",
    "unidade",
    "quantidade_licitada",
    "valor_unitario_estimado",
    "quantidade_contratada",
    "valor_unitario_contratado",
    "valor_total_contratado",
    "cpf_cnpj_fornecedor",
    "nome_fornecedor",
    "id_contrato",
    "ano_contrato",
    "tipo_contrato",
    "situacao_item",
    "observacao",
    "natureza_despesa",
    "programa_trabalho"
FROM "base-dos-dados-br-camara-dados-abertos--licitacao-item"
