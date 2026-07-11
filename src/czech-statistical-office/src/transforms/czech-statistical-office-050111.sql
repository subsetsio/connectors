-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    "esa_kod",
    CAST("sektor_cis" AS BIGINT) AS sektor_cis,
    CAST("sektor_kod" AS BIGINT) AS sektor_kod,
    CAST("oceneni_cis" AS BIGINT) AS oceneni_cis,
    "oceneni_kod",
    CAST("casz_cis" AS BIGINT) AS casz_cis,
    "casz_kod",
    CAST("rok" AS BIGINT) AS rok,
    CAST("rok_baz" AS BIGINT) AS rok_baz,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "stapro_txt",
    "mj_txt",
    "sektor_txt",
    "oceneni_txt",
    "casz_txt",
    "uzemi_txt"
FROM "czech-statistical-office-050111"
