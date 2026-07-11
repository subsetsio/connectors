-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_member",
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS BIGINT) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    "stapro_txt",
    CAST("rok" AS BIGINT) AS rok,
    strptime("datum", '%Y-%m-%d')::DATE AS datum,
    CAST("vuzemi_cis" AS BIGINT) AS vuzemi_cis,
    CAST("vuzemi_kod" AS BIGINT) AS vuzemi_kod,
    "vuzemi_txt",
    CAST("so_orp" AS BIGINT) AS so_orp,
    "so_orp_text",
    CAST("okres" AS BIGINT) AS okres,
    "okres_text",
    CAST("kraj" AS BIGINT) AS kraj,
    "kraj_text"
FROM "czech-statistical-office-170240-17"
