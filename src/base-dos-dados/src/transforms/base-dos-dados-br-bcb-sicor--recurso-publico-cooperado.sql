-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_referencia_bacen",
    "numero_ordem",
    "tipo_cpf_cnpj",
    "tipo_pessoa",
    "valor_parcela"
FROM "base-dos-dados-br-bcb-sicor--recurso-publico-cooperado"
