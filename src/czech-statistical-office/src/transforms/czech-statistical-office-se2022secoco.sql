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
    CAST("OBVOD" AS BIGINT) AS obvod,
    CAST("MINOKRSEK1" AS BIGINT) AS minokrsek1,
    CAST("MAXOKRSEK1" AS BIGINT) AS maxokrsek1,
    CAST("MINOKRSEK2" AS BIGINT) AS minokrsek2,
    CAST("MAXOKRSEK2" AS BIGINT) AS maxokrsek2,
    CAST("MINOKRSEK3" AS BIGINT) AS minokrsek3,
    CAST("MAXOKRSEK3" AS BIGINT) AS maxokrsek3,
    CAST("MINOKRSEK4" AS BIGINT) AS minokrsek4,
    CAST("MAXOKRSEK4" AS BIGINT) AS maxokrsek4,
    CAST("MINOKRSEK5" AS BIGINT) AS minokrsek5,
    CAST("MAXOKRSEK5" AS BIGINT) AS maxokrsek5,
    CAST("MINOKRSEK6" AS BIGINT) AS minokrsek6,
    CAST("MAXOKRSEK6" AS BIGINT) AS maxokrsek6,
    CAST("MINOKRSEK7" AS BIGINT) AS minokrsek7,
    CAST("MAXOKRSEK7" AS BIGINT) AS maxokrsek7,
    CAST("MINOKRSEK8" AS BIGINT) AS minokrsek8,
    CAST("MAXOKRSEK8" AS BIGINT) AS maxokrsek8,
    CAST("MINOKRSEK9" AS BIGINT) AS minokrsek9,
    CAST("MAXOKRSEK9" AS BIGINT) AS maxokrsek9,
    CAST("MINOKRSE10" AS BIGINT) AS minokrse10,
    CAST("MAXOKRSE10" AS BIGINT) AS maxokrse10,
    CAST("OBEC_PREZ" AS BIGINT) AS obec_prez
FROM "czech-statistical-office-se2022secoco"
