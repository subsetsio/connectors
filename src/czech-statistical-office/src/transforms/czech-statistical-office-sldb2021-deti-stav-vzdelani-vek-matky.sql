-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("ukaz_kod" AS BIGINT) AS ukaz_kod,
    CAST("stav_zeny_cis" AS BIGINT) AS stav_zeny_cis,
    CAST("stav_zeny_kod" AS BIGINT) AS stav_zeny_kod,
    CAST("vzdelani_zeny_cis" AS BIGINT) AS vzdelani_zeny_cis,
    "vzdelani_zeny_kod",
    CAST("vek_zeny_cis" AS BIGINT) AS vek_zeny_cis,
    CAST("vek_zeny_kod" AS BIGINT) AS vek_zeny_kod,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    CAST("sldb_rok" AS BIGINT) AS sldb_rok,
    strptime("sldb_datum", '%Y-%m-%d')::DATE AS sldb_datum,
    "ukaz_txt",
    "stav_zeny_txt",
    "vzdelani_zeny_txt",
    "vek_zeny_txt",
    "uzemi_txt"
FROM "czech-statistical-office-sldb2021-deti-stav-vzdelani-vek-matky"
