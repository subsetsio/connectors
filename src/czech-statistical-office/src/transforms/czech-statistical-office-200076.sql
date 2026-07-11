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
    CAST("misto_cis" AS BIGINT) AS misto_cis,
    "misto_kod",
    CAST("stavprace_cis" AS BIGINT) AS stavprace_cis,
    "stavprace_kod",
    CAST("obdobiod" AS TIMESTAMP) AS obdobiod,
    CAST("obdobido" AS TIMESTAMP) AS obdobido,
    CAST("ctvrtleti" AS BIGINT) AS ctvrtleti,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "stapro_txt",
    "mj_txt",
    "misto_txt",
    "stavprace_txt"
FROM "czech-statistical-office-200076"
