-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano_licitacao",
    "id_licitacao",
    "ano_contrato",
    "id_contrato",
    "tipo_contrato",
    "situacao_contrato",
    "descricao",
    strptime("data_assinatura", '%Y-%m-%d')::DATE AS data_assinatura,
    strptime("data_publicacao", '%Y-%m-%d')::DATE AS data_publicacao,
    strptime("data_inicio_contrato", '%Y-%m-%d')::DATE AS data_inicio_contrato,
    strptime("data_fim_contrato", '%Y-%m-%d')::DATE AS data_fim_contrato,
    strptime("data_fim_ultima_vigencia", '%Y-%m-%d')::DATE AS data_fim_ultima_vigencia,
    "nome_fornecedor",
    "endereco_fornecedor",
    "cidade_fornecedor",
    "sigla_uf_fornecedor",
    "cpf_cnpj_fornecedor",
    "valor_original",
    "valor_total"
FROM "base-dos-dados-br-camara-dados-abertos--licitacao-contrato"
