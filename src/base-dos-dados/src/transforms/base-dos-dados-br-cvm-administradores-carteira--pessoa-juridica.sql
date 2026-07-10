-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cnpj",
    "denominacao_social",
    "denominacao_comercial",
    strptime("data_registro", '%Y-%m-%d')::DATE AS data_registro,
    strptime("data_cancelamento", '%Y-%m-%d')::DATE AS data_cancelamento,
    "motivo_cancelamento",
    "situacao",
    strptime("data_inicio_situacao", '%Y-%m-%d')::DATE AS data_inicio_situacao,
    "categoria_registro",
    "subcategoria_registro",
    "controle_acionario",
    "tipo_endereco",
    "logradouro",
    "complemento",
    "bairro",
    "municipio",
    "sigla_uf",
    "cep",
    "ddd",
    "telefone",
    "valor_patrimonial_liquido",
    strptime("data_patrimonio_liquido", '%Y-%m-%d')::DATE AS data_patrimonio_liquido,
    "email",
    "website"
FROM "base-dos-dados-br-cvm-administradores-carteira--pessoa-juridica"
