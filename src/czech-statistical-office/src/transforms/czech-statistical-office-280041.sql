-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    "duvernost",
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("dnn_cis" AS BIGINT) AS dnn_cis,
    CAST("dnn_kod" AS BIGINT) AS dnn_kod,
    CAST("sektor_cis" AS BIGINT) AS sektor_cis,
    CAST("sektor_kod" AS BIGINT) AS sektor_kod,
    CAST("ozp_cis" AS BIGINT) AS ozp_cis,
    CAST("ozp_kod" AS BIGINT) AS ozp_kod,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "ukazatel_txt",
    "ozp_txt",
    "uzemi_txt",
    "typ_uzemi"
FROM "czech-statistical-office-280041"
