-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_member",
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    "duvernost",
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("kat_cis" AS BIGINT) AS kat_cis,
    "kat_kod",
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    "uzemi_kod",
    "uzemi_txt",
    "stapro_txt",
    "kat_txt"
FROM "czech-statistical-office-020055"
