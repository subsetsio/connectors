-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("dd_cis" AS BIGINT) AS dd_cis,
    "dd_kod",
    CAST("druhtez_cis" AS BIGINT) AS druhtez_cis,
    CAST("druhtez_kod" AS BIGINT) AS druhtez_kod,
    CAST("prictez_cis" AS BIGINT) AS prictez_cis,
    CAST("prictez_kod" AS BIGINT) AS prictez_kod,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "dd_txt",
    "druhtez_txt",
    "prictez_txt",
    CAST("ELPRO_ID" AS BIGINT) AS elpro_id
FROM "czech-statistical-office-100013"
