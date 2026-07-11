-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_member",
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("mj_cis" AS BIGINT) AS mj_cis,
    CAST("mj_kod" AS BIGINT) AS mj_kod,
    CAST("velskup_cis" AS BIGINT) AS velskup_cis,
    CAST("velskup_kod" AS BIGINT) AS velskup_kod,
    CAST("vuzemi_cis" AS BIGINT) AS vuzemi_cis,
    CAST("vuzemi_kod" AS BIGINT) AS vuzemi_kod,
    CAST("rok" AS BIGINT) AS rok,
    strptime("casref_do", '%Y-%m-%d')::DATE AS casref_do,
    "vuzemi_txt",
    "stapro_txt",
    "mj_txt",
    "velskup_txt"
FROM "czech-statistical-office-340130"
