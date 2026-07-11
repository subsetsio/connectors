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
    CAST("bydliste_cis" AS BIGINT) AS bydliste_cis,
    CAST("bydliste_kod" AS BIGINT) AS bydliste_kod,
    CAST("cil_dojizdky_cis" AS BIGINT) AS cil_dojizdky_cis,
    CAST("cil_dojizdky_kod" AS BIGINT) AS cil_dojizdky_kod,
    CAST("pohlavi_cis" AS BIGINT) AS pohlavi_cis,
    CAST("pohlavi_kod" AS BIGINT) AS pohlavi_kod,
    CAST("sldb_rok" AS BIGINT) AS sldb_rok,
    strptime("sldb_datum", '%Y-%m-%d')::DATE AS sldb_datum,
    "ukaz_txt",
    "aktivita_txt",
    "bydliste_txt",
    "bydliste_typ",
    "cil_dojizdky_txt",
    "cil_dojizdky_typ",
    "pohlavi_txt"
FROM "czech-statistical-office-sldb2021-vyjizdka-pracoviste-cil-pohlavi"
