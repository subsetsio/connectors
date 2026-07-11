-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("SPKVANTIL_cis" AS BIGINT) AS spkvantil_cis,
    "SPKVANTIL_kod" AS spkvantil_kod,
    CAST("POHLAVI_cis" AS BIGINT) AS pohlavi_cis,
    CAST("POHLAVI_kod" AS BIGINT) AS pohlavi_kod,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "STAPRO_TXT" AS stapro_txt,
    "uzemi_txt",
    "SPKVANTIL_txt" AS spkvantil_txt,
    "POHLAVI_txt" AS pohlavi_txt
FROM "czech-statistical-office-110080"
