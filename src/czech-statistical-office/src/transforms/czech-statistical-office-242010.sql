-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("mj_cis" AS BIGINT) AS mj_cis,
    "mj_kod",
    CAST("czem_cis" AS BIGINT) AS czem_cis,
    "czem_kod",
    CAST("vuzemi_cis" AS BIGINT) AS vuzemi_cis,
    CAST("vuzemi_kod" AS BIGINT) AS vuzemi_kod,
    CAST("rok" AS BIGINT) AS rok,
    "mesic",
    "stapro_txt",
    "czem_txt"
FROM "czech-statistical-office-242010"
