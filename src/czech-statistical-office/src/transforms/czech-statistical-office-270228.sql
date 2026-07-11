-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("mj_cis" AS BIGINT) AS mj_cis,
    CAST("mj_kod" AS BIGINT) AS mj_kod,
    CAST("druhzplod_cis" AS BIGINT) AS druhzplod_cis,
    CAST("druhzplod_kod" AS BIGINT) AS druhzplod_kod,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "uzemi_txt",
    "druhzplod_txt"
FROM "czech-statistical-office-270228"
