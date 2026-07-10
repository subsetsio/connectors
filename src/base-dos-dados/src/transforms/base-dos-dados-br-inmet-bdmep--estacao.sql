-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_municipio",
    "id_estacao",
    "estacao",
    strptime("data_fundacao", '%Y-%m-%d')::DATE AS data_fundacao,
    "latitude",
    "longitude",
    "altitude"
FROM "base-dos-dados-br-inmet-bdmep--estacao"
