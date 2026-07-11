-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified for this upstream table; treat rows as source observations and avoid assuming uniqueness without applying source-specific dimensions.
SELECT
    "source_member",
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("tb_cis" AS BIGINT) AS tb_cis,
    CAST("tb_kod" AS BIGINT) AS tb_kod,
    CAST("vuzemi_cis" AS BIGINT) AS vuzemi_cis,
    CAST("vuzemi_kod" AS BIGINT) AS vuzemi_kod,
    CAST("rok" AS BIGINT) AS rok,
    strptime("casref_od", '%Y-%m-%d')::DATE AS casref_od,
    strptime("casref_do", '%Y-%m-%d')::DATE AS casref_do,
    "stapro_txt",
    "tb_txt",
    "vuzemi_txt"
FROM "czech-statistical-office-200068"
