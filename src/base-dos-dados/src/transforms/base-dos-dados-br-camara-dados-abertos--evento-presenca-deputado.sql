-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_evento",
    strptime("data_inicio", '%Y-%m-%d')::DATE AS data_inicio,
    "horario_inicio",
    "id_deputado"
FROM "base-dos-dados-br-camara-dados-abertos--evento-presenca-deputado"
