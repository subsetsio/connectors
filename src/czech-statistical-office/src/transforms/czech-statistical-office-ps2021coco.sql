-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("KRAJ" AS BIGINT) AS kraj,
    CAST("OKRES" AS BIGINT) AS okres,
    CAST("CPOU" AS BIGINT) AS cpou,
    CAST("ORP" AS BIGINT) AS orp,
    CAST("OBEC" AS BIGINT) AS obec,
    "NAZEVOBCE" AS nazevobce,
    CAST("VOLKRAJ" AS BIGINT) AS volkraj,
    CAST("MINOKRSEK1" AS BIGINT) AS minokrsek1,
    CAST("MAXOKRSEK1" AS BIGINT) AS maxokrsek1,
    CAST("OBEC_PREZ" AS BIGINT) AS obec_prez
FROM "czech-statistical-office-ps2021coco"
