-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified for this upstream table; treat rows as source observations and avoid assuming uniqueness without applying source-specific dimensions.
SELECT
    CAST("DATUMVOLEB" AS BIGINT) AS datumvoleb,
    CAST("OKRES" AS BIGINT) AS okres,
    CAST("KODZASTUP" AS BIGINT) AS kodzastup,
    CAST("COBVODU" AS BIGINT) AS cobvodu,
    CAST("POR_STR_HL" AS BIGINT) AS por_str_hl,
    CAST("OSTRANA" AS BIGINT) AS ostrana,
    CAST("PORCISLO" AS BIGINT) AS porcislo,
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
    CAST("POCHLASU" AS BIGINT) AS pochlasu,
    "PRESKOCENI" AS preskoceni,
    CAST("POCPROCVSE" AS DOUBLE) AS pocprocvse,
    "MANDAT" AS mandat,
    CAST("PORADIMAND" AS BIGINT) AS poradimand,
    CAST("PORADINAHR" AS BIGINT) AS poradinahr
FROM "czech-statistical-office-kv2022kvrk"
