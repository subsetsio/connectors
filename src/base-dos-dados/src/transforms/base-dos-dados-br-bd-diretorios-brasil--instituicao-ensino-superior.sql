-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_ies",
    "nome",
    "tipo_instituicao",
    "rede",
    "situacao_funcionamento",
    "id_municipio",
    "sigla_uf"
FROM "base-dos-dados-br-bd-diretorios-brasil--instituicao-ensino-superior"
