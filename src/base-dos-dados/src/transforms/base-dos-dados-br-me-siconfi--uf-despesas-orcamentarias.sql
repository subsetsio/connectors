-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "sigla_uf",
    "id_uf",
    "estagio",
    "portaria",
    "conta",
    "estagio_bd",
    "id_conta_bd",
    "conta_bd",
    "valor"
FROM "base-dos-dados-br-me-siconfi--uf-despesas-orcamentarias"
