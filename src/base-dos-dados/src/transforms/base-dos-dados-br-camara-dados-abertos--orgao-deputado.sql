-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_orgao",
    "nome",
    "sigla",
    "nome_deputado",
    "cargo",
    "sigla_uf",
    strptime("data_inicio", '%Y-%m-%d')::DATE AS data_inicio,
    strptime("data_final", '%Y-%m-%d')::DATE AS data_final,
    "sigla_partido"
FROM "base-dos-dados-br-camara-dados-abertos--orgao-deputado"
