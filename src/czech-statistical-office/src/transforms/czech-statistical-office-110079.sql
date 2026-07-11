-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("mj_cis" AS BIGINT) AS mj_cis,
    "mj_kod",
    CAST("typosoby_kod" AS BIGINT) AS typosoby_kod,
    CAST("odvetvi_cis" AS BIGINT) AS odvetvi_cis,
    "odvetvi_kod",
    CAST("rok" AS BIGINT) AS rok,
    CAST("ctvrtleti" AS BIGINT) AS ctvrtleti,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "stapro_txt",
    "mj_txt",
    "typosoby_txt",
    "odvetvi_txt"
FROM "czech-statistical-office-110079"
