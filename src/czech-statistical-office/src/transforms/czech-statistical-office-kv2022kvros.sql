-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified for this upstream table; treat rows as source observations and avoid assuming uniqueness without applying source-specific dimensions.
SELECT
    CAST("DATUMVOLEB" AS BIGINT) AS datumvoleb,
    CAST("OKRES" AS BIGINT) AS okres,
    CAST("KODZASTUP" AS BIGINT) AS kodzastup,
    "NAZEVZAST" AS nazevzast,
    CAST("COBVODU" AS BIGINT) AS cobvodu,
    CAST("POR_STR_HL" AS BIGINT) AS por_str_hl,
    CAST("OSTRANA" AS BIGINT) AS ostrana,
    CAST("VSTRANA" AS BIGINT) AS vstrana,
    "NAZEVCELK" AS nazevcelk,
    "ZKRATKAO30" AS zkratkao30,
    "ZKRATKAO8" AS zkratkao8,
    CAST("POCSTR_SLO" AS BIGINT) AS pocstr_slo,
    "SLOZENI" AS slozeni,
    CAST("HLASY_STR" AS BIGINT) AS hlasy_str,
    CAST("PROCHLSTR" AS DOUBLE) AS prochlstr,
    CAST("MAND_STR" AS BIGINT) AS mand_str
FROM "czech-statistical-office-kv2022kvros"
