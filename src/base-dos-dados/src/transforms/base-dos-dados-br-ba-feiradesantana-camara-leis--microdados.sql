-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "titulo",
    "categoria",
    "resumo",
    "texto"
FROM "base-dos-dados-br-ba-feiradesantana-camara-leis--microdados"
