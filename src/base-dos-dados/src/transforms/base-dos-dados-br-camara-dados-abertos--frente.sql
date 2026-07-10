-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_frente",
    "titulo",
    strptime("data_criacao", '%Y-%m-%d')::DATE AS data_criacao,
    "id_legislatura",
    "telefone",
    "situacao",
    "url_documento",
    "id_coordenador",
    "nome_coordenador",
    "url_foto_coordenador"
FROM "base-dos-dados-br-camara-dados-abertos--frente"
