-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    "duvernost",
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("spjmen_cis" AS BIGINT) AS spjmen_cis,
    "spjmen_kod",
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "uzemi_txt",
    "stapro_txt",
    "spjmen_txt",
    CAST("mesic" AS BIGINT) AS mesic
FROM "czech-statistical-office-260017"
