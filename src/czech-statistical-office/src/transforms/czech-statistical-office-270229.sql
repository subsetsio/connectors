-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("MJ_CIS" AS BIGINT) AS mj_cis,
    CAST("MJ_KOD" AS BIGINT) AS mj_kod,
    CAST("DRUHZPLOD_cis" AS BIGINT) AS druhzplod_cis,
    CAST("DRUHZPLOD_kod" AS BIGINT) AS druhzplod_kod,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "STAPRO_TXT" AS stapro_txt,
    "uzemi_txt",
    "DRUHZPLOD_txt" AS druhzplod_txt
FROM "czech-statistical-office-270229"
