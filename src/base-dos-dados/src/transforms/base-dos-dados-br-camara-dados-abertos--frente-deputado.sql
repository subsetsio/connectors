-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_frente",
    "titulo_deputado",
    "id_deputado",
    "nome_deputado",
    "url_foto_deputado"
FROM "base-dos-dados-br-camara-dados-abertos--frente-deputado"
