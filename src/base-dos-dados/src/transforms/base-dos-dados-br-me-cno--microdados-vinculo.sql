-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_cno",
    strptime("data_inicio", '%Y-%m-%d')::DATE AS data_inicio,
    strptime("data_fim", '%Y-%m-%d')::DATE AS data_fim,
    strptime("data_registro", '%Y-%m-%d')::DATE AS data_registro,
    "qualificacao_responsavel",
    "ni_responsavel"
FROM "base-dos-dados-br-me-cno--microdados-vinculo"
