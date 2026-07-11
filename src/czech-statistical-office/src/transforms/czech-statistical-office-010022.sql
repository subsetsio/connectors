-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    "ucel_tep",
    CAST("ucel_cis" AS BIGINT) AS ucel_cis,
    "ucel_kod",
    "casz_kod",
    CAST("mesic" AS BIGINT) AS mesic,
    CAST("rok" AS BIGINT) AS rok,
    strptime("obdobiod", '%Y-%m-%d')::DATE AS obdobiod,
    strptime("obdobido", '%Y-%m-%d')::DATE AS obdobido,
    strptime("bazobdobiod", '%Y-%m-%d')::DATE AS bazobdobiod,
    strptime("bazobdobido", '%Y-%m-%d')::DATE AS bazobdobido,
    "ucel_txt",
    "casz_txt"
FROM "czech-statistical-office-010022"
