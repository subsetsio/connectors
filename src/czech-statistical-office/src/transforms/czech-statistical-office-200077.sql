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
    CAST("mj_cis" AS BIGINT) AS mj_cis,
    "mj_kod",
    CAST("typstavby_cis" AS BIGINT) AS typstavby_cis,
    CAST("typstavby_kod" AS BIGINT) AS typstavby_kod,
    CAST("smer_cis" AS BIGINT) AS smer_cis,
    CAST("smer_kod" AS BIGINT) AS smer_kod,
    CAST("mesicod" AS BIGINT) AS mesicod,
    CAST("mesicdo" AS BIGINT) AS mesicdo,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "uzemi_txt",
    "stapro_txt",
    "mj_txt",
    "typstavby_txt",
    "smer_txt"
FROM "czech-statistical-office-200077"
