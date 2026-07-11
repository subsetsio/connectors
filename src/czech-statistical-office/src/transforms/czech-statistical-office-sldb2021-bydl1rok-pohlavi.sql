-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("ukaz_kod" AS BIGINT) AS ukaz_kod,
    CAST("bydl_1rok_cis" AS BIGINT) AS bydl_1rok_cis,
    "bydl_1rok_kod",
    CAST("bydl_cleneni_typ" AS BIGINT) AS bydl_cleneni_typ,
    CAST("pohlavi_cis" AS BIGINT) AS pohlavi_cis,
    CAST("pohlavi_kod" AS BIGINT) AS pohlavi_kod,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    CAST("sldb_rok" AS BIGINT) AS sldb_rok,
    strptime("sldb_datum", '%Y-%m-%d')::DATE AS sldb_datum,
    "ukaz_txt",
    "bydl_1rok_txt",
    "bydl_cleneni_txt",
    "pohlavi_txt",
    "uzemi_txt"
FROM "czech-statistical-office-sldb2021-bydl1rok-pohlavi"
