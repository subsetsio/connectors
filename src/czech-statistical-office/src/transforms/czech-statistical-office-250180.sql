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
    CAST("ekak_cis" AS BIGINT) AS ekak_cis,
    CAST("ekak_kod" AS BIGINT) AS ekak_kod,
    CAST("pohlavi_cis" AS BIGINT) AS pohlavi_cis,
    CAST("pohlavi_kod" AS BIGINT) AS pohlavi_kod,
    CAST("rok" AS BIGINT) AS rok,
    CAST("ctvrtleti" AS BIGINT) AS ctvrtleti,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "uzemi_txt",
    "stapro_txt",
    "mj_txt",
    "pohlavi_txt"
FROM "czech-statistical-office-250180"
