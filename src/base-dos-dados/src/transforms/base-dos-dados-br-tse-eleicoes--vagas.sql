-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "id_eleicao",
    "tipo_eleicao",
    strptime("data_eleicao", '%Y-%m-%d')::DATE AS data_eleicao,
    "sigla_uf",
    "id_municipio",
    "id_municipio_tse",
    "cargo",
    "vagas"
FROM "base-dos-dados-br-tse-eleicoes--vagas"
