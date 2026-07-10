-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_distrito",
    "nome",
    "id_municipio",
    "sigla_uf"
FROM "base-dos-dados-br-bd-diretorios-brasil--distrito-2000"
