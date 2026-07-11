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
    CAST("stobcan_cis" AS BIGINT) AS stobcan_cis,
    CAST("stobcan_kod" AS BIGINT) AS stobcan_kod,
    CAST("vek_cis" AS BIGINT) AS vek_cis,
    CAST("vek_kod" AS BIGINT) AS vek_kod,
    CAST("rok" AS BIGINT) AS rok,
    CAST("vuzemi_cis" AS BIGINT) AS vuzemi_cis,
    CAST("vuzemi_kod" AS BIGINT) AS vuzemi_kod,
    CAST("kraj_cis" AS BIGINT) AS kraj_cis,
    CAST("kraj_kod" AS BIGINT) AS kraj_kod,
    "vuzemi_txt",
    "kraj_txt",
    "pohlavi_txt",
    "stobcan_txt",
    "vek_txt"
FROM "czech-statistical-office-290038r23"
