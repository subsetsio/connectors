-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_member",
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("pohlavi_cis" AS BIGINT) AS pohlavi_cis,
    CAST("pohlavi_kod" AS BIGINT) AS pohlavi_kod,
    CAST("ps_cis" AS BIGINT) AS ps_cis,
    "ps_kod",
    CAST("ps0_cis" AS BIGINT) AS ps0_cis,
    "ps0_kod",
    CAST("vuzemi_cis" AS BIGINT) AS vuzemi_cis,
    CAST("vuzemi_kod" AS BIGINT) AS vuzemi_kod,
    CAST("rok" AS BIGINT) AS rok,
    "pohlavi_txt",
    "ps_txt",
    "ps0_txt",
    "vuzemi_txt"
FROM "czech-statistical-office-130143"
