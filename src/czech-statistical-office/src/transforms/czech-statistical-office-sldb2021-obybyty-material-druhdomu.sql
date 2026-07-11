-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("ukaz_kod" AS BIGINT) AS ukaz_kod,
    CAST("material_cis" AS BIGINT) AS material_cis,
    CAST("material_kod" AS BIGINT) AS material_kod,
    CAST("druhdomu_cis" AS BIGINT) AS druhdomu_cis,
    CAST("druhdomu_kod" AS BIGINT) AS druhdomu_kod,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    CAST("sldb_rok" AS BIGINT) AS sldb_rok,
    strptime("sldb_datum", '%Y-%m-%d')::DATE AS sldb_datum,
    "ukaz_txt",
    "material_txt",
    "druhdomu_txt",
    "uzemi_txt",
    "uzemi_typ"
FROM "czech-statistical-office-sldb2021-obybyty-material-druhdomu"
