-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("KSTRANA" AS BIGINT) AS kstrana,
    CAST("VSTRANA" AS BIGINT) AS vstrana,
    "NAZEVCELK" AS nazevcelk,
    "NAZEV_STRK" AS nazev_strk,
    "ZKRATKAK30" AS zkratkak30,
    "ZKRATKAK8" AS zkratkak8,
    CAST("POCSTRVKO" AS BIGINT) AS pocstrvko,
    "SLOZENI" AS slozeni,
    "STAVREG" AS stavreg,
    "PLAT_STR" AS plat_str,
    "SLOZNEPLAT" AS slozneplat,
    CAST("POCMANDCR" AS BIGINT) AS pocmandcr,
    "NAZEVPLNY" AS nazevplny
FROM "czech-statistical-office-kz2024kzrkl-s"
