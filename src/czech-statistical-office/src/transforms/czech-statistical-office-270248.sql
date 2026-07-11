-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("mj_cis" AS BIGINT) AS mj_cis,
    CAST("mj_kod" AS BIGINT) AS mj_kod,
    CAST("druhzvire_cis" AS BIGINT) AS druhzvire_cis,
    CAST("druhzvire_kod" AS BIGINT) AS druhzvire_kod,
    CAST("vek_cis" AS BIGINT) AS vek_cis,
    CAST("vek_kod" AS BIGINT) AS vek_kod,
    CAST("vekmes_cis" AS BIGINT) AS vekmes_cis,
    CAST("vekmes_kod" AS BIGINT) AS vekmes_kod,
    CAST("hmotkg_cis" AS BIGINT) AS hmotkg_cis,
    CAST("hmotkg_kod" AS BIGINT) AS hmotkg_kod,
    strptime("datum", '%Y-%m-%d')::DATE AS datum,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "uzemi_txt",
    "mj_txt",
    "key",
    "alttext_cz",
    "alttext_en"
FROM "czech-statistical-office-270248"
