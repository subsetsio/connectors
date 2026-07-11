-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("pohlavi_cis" AS BIGINT) AS pohlavi_cis,
    CAST("pohlavi_kod" AS BIGINT) AS pohlavi_kod,
    CAST("vek_cis" AS BIGINT) AS vek_cis,
    CAST("vek_kod" AS BIGINT) AS vek_kod,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    strptime("obdobi", '%Y-%m-%d')::DATE AS obdobi,
    "pohlavi_txt",
    CAST("vek_txt" AS BIGINT) AS vek_txt,
    "uzemi_txt",
    "uzemi_typ"
FROM "czech-statistical-office-130181r23"
