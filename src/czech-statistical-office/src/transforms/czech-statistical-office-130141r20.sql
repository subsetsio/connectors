-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    "vuk",
    "vuk_text",
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("vuzemi_cis" AS BIGINT) AS vuzemi_cis,
    CAST("vuzemi_kod" AS BIGINT) AS vuzemi_kod,
    CAST("rok" AS BIGINT) AS rok,
    strptime("casref_od", '%Y-%m-%d')::DATE AS casref_od,
    strptime("casref_do", '%Y-%m-%d')::DATE AS casref_do,
    "vuzemi_txt"
FROM "czech-statistical-office-130141r20"
