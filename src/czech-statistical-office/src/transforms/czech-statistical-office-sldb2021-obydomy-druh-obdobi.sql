-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("ukaz_kod" AS BIGINT) AS ukaz_kod,
    CAST("druh_cis" AS BIGINT) AS druh_cis,
    CAST("druh_kod" AS BIGINT) AS druh_kod,
    CAST("obdobi_cis" AS BIGINT) AS obdobi_cis,
    CAST("obdobi_kod" AS BIGINT) AS obdobi_kod,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    CAST("sldb_rok" AS BIGINT) AS sldb_rok,
    strptime("sldb_datum", '%Y-%m-%d')::DATE AS sldb_datum,
    "ukaz_txt",
    "druh_txt",
    "obdobi_txt",
    "uzemi_txt",
    "uzemi_typ"
FROM "czech-statistical-office-sldb2021-obydomy-druh-obdobi"
