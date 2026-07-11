-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("ekakocd_cis" AS BIGINT) AS ekakocd_cis,
    CAST("ekakocd_kod" AS BIGINT) AS ekakocd_kod,
    CAST("pvdom_cis" AS BIGINT) AS pvdom_cis,
    CAST("pvdom_kod" AS BIGINT) AS pvdom_kod,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "stapro_txt",
    "ekakocd_txt",
    "pvdom_txt"
FROM "czech-statistical-office-160061"
