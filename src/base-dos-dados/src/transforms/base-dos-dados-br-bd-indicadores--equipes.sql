-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_pessoa",
    strptime("data_inicio", '%Y-%m-%d')::DATE AS data_inicio,
    strptime("data_fim", '%Y-%m-%d')::DATE AS data_fim,
    "equipe",
    "nivel",
    "cargo"
FROM "base-dos-dados-br-bd-indicadores--equipes"
