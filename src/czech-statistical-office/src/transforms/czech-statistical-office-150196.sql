-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("casz_cis" AS BIGINT) AS casz_cis,
    "casz_kod",
    CAST("cznace_cis" AS BIGINT) AS cznace_cis,
    "cznace_kod",
    CAST("mesic" AS BIGINT) AS mesic,
    CAST("rok" AS BIGINT) AS rok,
    CAST("mesicz" AS BIGINT) AS mesicz,
    CAST("rokz" AS BIGINT) AS rokz,
    "stapro_txt",
    "casz_txt",
    "cznace_txt"
FROM "czech-statistical-office-150196"
