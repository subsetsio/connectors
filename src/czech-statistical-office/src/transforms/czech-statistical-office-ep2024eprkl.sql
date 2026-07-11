-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("ESTRANA" AS BIGINT) AS estrana,
    CAST("VSTRANA" AS BIGINT) AS vstrana,
    "NAZEVCELK" AS nazevcelk,
    "NAZEV_STRE" AS nazev_stre,
    "ZKRATKAE30" AS zkratkae30,
    "ZKRATKAE8" AS zkratkae8,
    CAST("POCSTRVKO" AS BIGINT) AS pocstrvko,
    "SLOZENI" AS slozeni,
    CAST("STAVREG" AS BIGINT) AS stavreg,
    "PLAT_STR" AS plat_str,
    "SLOZNEPLAT" AS slozneplat,
    CAST("POCMANDCR" AS BIGINT) AS pocmandcr,
    "NAZEVPLNY" AS nazevplny
FROM "czech-statistical-office-ep2024eprkl"
