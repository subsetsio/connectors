-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_orgao",
    "sigla",
    "apelido",
    "nome",
    "cod_tipo_orgao",
    "tipo_orgao",
    "casa",
    "sala",
    "cod_situacao",
    "descricao_situacao",
    CAST("data_inicio" AS TIMESTAMP) AS data_inicio,
    CAST("data_instalacao" AS TIMESTAMP) AS data_instalacao,
    CAST("data_fim" AS TIMESTAMP) AS data_fim,
    "uri",
    CAST("capture_date" AS TIMESTAMP) AS capture_date
FROM "base-dos-dados-br-camara-atividade-legislativa--orgaos"
