-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("ukaz_kod" AS BIGINT) AS ukaz_kod,
    CAST("aktivita_cis" AS BIGINT) AS aktivita_cis,
    CAST("aktivita_kod" AS BIGINT) AS aktivita_kod,
    CAST("kraj_dojizdky_cis" AS BIGINT) AS kraj_dojizdky_cis,
    CAST("kraj_dojizdky_kod" AS BIGINT) AS kraj_dojizdky_kod,
    CAST("pohlavi_cis" AS BIGINT) AS pohlavi_cis,
    CAST("pohlavi_kod" AS BIGINT) AS pohlavi_kod,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    CAST("sldb_rok" AS BIGINT) AS sldb_rok,
    strptime("sldb_datum", '%Y-%m-%d')::DATE AS sldb_datum,
    "ukaz_txt",
    "aktivita_txt",
    "kraj_dojizdky_txt",
    "pohlavi_txt",
    "uzemi_txt",
    "uzemi_typ"
FROM "czech-statistical-office-sldb2021-vyjizdka-pracoviste-kraj-pohlavi"
