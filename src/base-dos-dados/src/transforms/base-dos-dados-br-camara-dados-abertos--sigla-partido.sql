-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sigla_partido_antiga",
    "sigla_partido_nova"
FROM "base-dos-dados-br-camara-dados-abertos--sigla-partido"
