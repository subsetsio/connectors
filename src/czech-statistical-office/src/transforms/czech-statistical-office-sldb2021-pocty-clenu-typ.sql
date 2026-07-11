-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("ukaz_kod" AS BIGINT) AS ukaz_kod,
    CAST("clenu_cis" AS BIGINT) AS clenu_cis,
    "clenu_kod",
    CAST("typ_cis" AS BIGINT) AS typ_cis,
    CAST("typ_kod" AS BIGINT) AS typ_kod,
    "typ_struktura",
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    CAST("sldb_rok" AS BIGINT) AS sldb_rok,
    strptime("sldb_datum", '%Y-%m-%d')::DATE AS sldb_datum,
    "ukaz_txt",
    "clenu_txt",
    "typ_txt",
    "uzemi_txt",
    "uzemi_typ"
FROM "czech-statistical-office-sldb2021-pocty-clenu-typ"
