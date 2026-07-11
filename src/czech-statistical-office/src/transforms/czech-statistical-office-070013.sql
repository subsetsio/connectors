-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    "stapro_txt",
    CAST("cznace_cis" AS BIGINT) AS cznace_cis,
    "cznace_kod",
    CAST("stocisteni_cis" AS BIGINT) AS stocisteni_cis,
    "stocisteni_kod",
    strptime("obdobiod", '%Y-%m-%d')::DATE AS obdobiod,
    strptime("obdobido", '%Y-%m-%d')::DATE AS obdobido,
    strptime("bazobdobiod", '%Y-%m-%d')::DATE AS bazobdobiod,
    strptime("bazobdobido", '%Y-%m-%d')::DATE AS bazobdobido,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "uzemi_txt",
    "cznace_txt",
    "stocisteni_txt"
FROM "czech-statistical-office-070013"
