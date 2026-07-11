-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    "duvernost",
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    "stapro_txt",
    CAST("kat_cis" AS BIGINT) AS kat_cis,
    CAST("kat_kod" AS BIGINT) AS kat_kod,
    CAST("uzemiz_cis" AS BIGINT) AS uzemiz_cis,
    CAST("uzemiz_kod" AS BIGINT) AS uzemiz_kod,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    "uzemi_kod",
    "uzemi_txt",
    "uzemi_typ"
FROM "czech-statistical-office-020050"
