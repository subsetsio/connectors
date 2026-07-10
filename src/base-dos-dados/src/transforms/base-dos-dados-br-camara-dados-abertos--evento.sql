-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_evento",
    "url_documento_pauta",
    strptime("data_inicio", '%Y-%m-%d')::DATE AS data_inicio,
    "horario_inicio",
    strptime("data_final", '%Y-%m-%d')::DATE AS data_final,
    "horario_final",
    "situacao",
    "descricao",
    "tipo",
    "local_externo",
    "nome_local"
FROM "base-dos-dados-br-camara-dados-abertos--evento"
