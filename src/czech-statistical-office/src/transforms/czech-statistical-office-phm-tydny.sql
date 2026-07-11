-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("ukazatel_kod" AS BIGINT) AS ukazatel_kod,
    CAST("polozka_cis" AS BIGINT) AS polozka_cis,
    "polozka_kod",
    "obdobi",
    CAST("rok" AS BIGINT) AS rok,
    "tyden",
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "ukazatel_txt",
    "polozka_txt"
FROM "czech-statistical-office-phm-tydny"
