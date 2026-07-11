-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("mj_cis" AS BIGINT) AS mj_cis,
    CAST("mj_kod" AS BIGINT) AS mj_kod,
    CAST("druhzvire_cis" AS BIGINT) AS druhzvire_cis,
    CAST("druhzvire_kod" AS BIGINT) AS druhzvire_kod,
    CAST("mesic" AS BIGINT) AS mesic,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "stapro_txt",
    "mj_txt",
    "uzemi_txt",
    "zviremaso_txt",
    "status_kod",
    "status_txt"
FROM "czech-statistical-office-270243"
