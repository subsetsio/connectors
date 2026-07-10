-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "orgao",
    "gestao",
    "unidade_gestora",
    "fonte_de_recursos",
    "receita",
    "arrecadado"
FROM "base-dos-dados-br-sp-gov-orcamento--receita-arrecadada"
