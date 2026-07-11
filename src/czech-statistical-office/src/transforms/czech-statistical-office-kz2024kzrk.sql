-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
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
    CAST("PSTRANA" AS BIGINT) AS pstrana,
    CAST("NSTRANA" AS BIGINT) AS nstrana,
    "PLATNOST" AS platnost,
    CAST("POCHLASU" AS BIGINT) AS pochlasu,
    "POCPROC" AS pocproc,
    "MANDAT" AS mandat,
    CAST("PORADIMAND" AS BIGINT) AS poradimand,
    CAST("PORADINAHR" AS BIGINT) AS poradinahr
FROM "czech-statistical-office-kz2024kzrk"
