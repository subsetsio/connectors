-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("OBVOD" AS BIGINT) AS obvod,
    CAST("CKAND" AS BIGINT) AS ckand,
    CAST("VSTRANA" AS BIGINT) AS vstrana,
    "JMENO" AS jmeno,
    "PRIJMENI" AS prijmeni,
    "TITULPRED" AS titulpred,
    "TITULZA" AS titulza,
    CAST("VEK" AS BIGINT) AS vek,
    "POVOLANI" AS povolani,
    "BYDLISTEN" AS bydlisten,
    CAST("PSTRANA" AS BIGINT) AS pstrana,
    CAST("NSTRANA" AS BIGINT) AS nstrana,
    "PLATNOST" AS platnost,
    CAST("HLASY_K1" AS BIGINT) AS hlasy_k1,
    CAST("PROC_K1" AS DOUBLE) AS proc_k1,
    CAST("URIZ_PR_K1" AS DOUBLE) AS uriz_pr_k1,
    CAST("ZVOLEN_K1" AS BIGINT) AS zvolen_k1,
    CAST("LOS_K1" AS BIGINT) AS los_k1,
    CAST("HLASY_K2" AS BIGINT) AS hlasy_k2,
    CAST("PROC_K2" AS DOUBLE) AS proc_k2,
    CAST("URIZ_PR_K2" AS DOUBLE) AS uriz_pr_k2,
    CAST("ZVOLEN_K2" AS BIGINT) AS zvolen_k2,
    CAST("LOS_K2" AS BIGINT) AS los_k2,
    "NAZEV_VS" AS nazev_vs
FROM "czech-statistical-office-se2024serk"
