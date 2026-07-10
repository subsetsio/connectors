-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nome",
    strptime("data_registro", '%Y-%m-%d')::DATE AS data_registro,
    strptime("data_cancelamento", '%Y-%m-%d')::DATE AS data_cancelamento,
    "motivo_cancelamento",
    "situacao",
    strptime("data_inicio_situacao", '%Y-%m-%d')::DATE AS data_inicio_situacao,
    "categoria_registro"
FROM "base-dos-dados-br-cvm-administradores-carteira--pessoa-fisica"
