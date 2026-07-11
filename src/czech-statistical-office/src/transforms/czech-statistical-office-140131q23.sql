-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_member",
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("aktivita_cis" AS BIGINT) AS aktivita_cis,
    CAST("aktivita_kod" AS BIGINT) AS aktivita_kod,
    CAST("forma_cis" AS BIGINT) AS forma_cis,
    CAST("forma_kod" AS BIGINT) AS forma_kod,
    CAST("vuzemi_cis" AS BIGINT) AS vuzemi_cis,
    CAST("vuzemi_kod" AS BIGINT) AS vuzemi_kod,
    strptime("casref", '%Y-%m-%d')::DATE AS casref,
    "aktivita_txt",
    "forma_txt",
    "vuzemi_txt"
FROM "czech-statistical-office-140131q23"
