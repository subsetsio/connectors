-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cnpj",
    "nome",
    "tipo"
FROM "base-dos-dados-br-cvm-administradores-carteira--responsavel"
