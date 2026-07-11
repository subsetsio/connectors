-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified for this upstream table; treat rows as source observations and avoid assuming uniqueness without applying source-specific dimensions.
SELECT
    "source_member",
    CAST("KRZAST" AS BIGINT) AS krzast,
    CAST("KSTRANA" AS BIGINT) AS kstrana,
    CAST("PORCISLO" AS BIGINT) AS porcislo,
    "JMENO" AS jmeno,
    "PRIJMENI" AS prijmeni,
    "TITULPRED" AS titulpred,
    "TITULZA" AS titulza,
    CAST("VEK" AS BIGINT) AS vek,
    "POVOLANI" AS povolani,
    "BYDLISTEN" AS bydlisten,
    CAST("BYDLISTEK" AS BIGINT) AS bydlistek,
    CAST("PSTRANA" AS BIGINT) AS pstrana,
    CAST("NSTRANA" AS BIGINT) AS nstrana,
    "PLATNOST" AS platnost,
    CAST("POCHLASU" AS BIGINT) AS pochlasu,
    "POCPROC" AS pocproc,
    "MANDAT" AS mandat,
    CAST("PORADIMAND" AS BIGINT) AS poradimand,
    CAST("PORADINAHR" AS BIGINT) AS poradinahr,
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
FROM "czech-statistical-office-kz2020reg"
