-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "matricula",
    "nome_deputado",
    "cpf_cnpj",
    "fornecedor",
    "tipo",
    "valor"
FROM "base-dos-dados-br-sp-alesp--despesas-gabinete-atual"
