-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "id_municipio",
    "categoria_produto",
    "tipo_produto",
    "subtipo_produto",
    "produto",
    "unidade",
    "quantidade",
    "valor"
FROM "base-dos-dados-br-ibge-pevs--producao-silvicultura"
