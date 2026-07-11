-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified for this upstream table; treat rows as source observations and avoid assuming uniqueness without applying source-specific dimensions.
SELECT
    "source_member",
    CAST("OBEC_PREZ" AS BIGINT) AS obec_prez,
    "NAZEVOBCE" AS nazevobce,
    CAST("KRAJ" AS BIGINT) AS kraj,
    CAST("OKRES" AS BIGINT) AS okres,
    CAST("CPOU" AS BIGINT) AS cpou,
    CAST("ORP" AS BIGINT) AS orp,
    CAST("OBEC" AS BIGINT) AS obec,
    CAST("MINOKRSEK1" AS BIGINT) AS minokrsek1,
    CAST("MAXOKRSEK1" AS BIGINT) AS maxokrsek1,
    CAST("NSTRANA" AS BIGINT) AS nstrana,
    "NAZEV_STRN" AS nazev_strn,
    "ZKRATKAN30" AS zkratkan30,
    "ZKRATKAN8" AS zkratkan8,
    CAST("PSTRANA" AS BIGINT) AS pstrana,
    "NAZEV_STRP" AS nazev_strp,
    "ZKRATKAP30" AS zkratkap30,
    "ZKRATKAP8" AS zkratkap8,
    CAST("NUMNUTS" AS BIGINT) AS numnuts,
    "NUTS" AS nuts,
    "NAZEVNUTS" AS nazevnuts,
    CAST("KODCIS" AS BIGINT) AS kodcis,
    CAST("CHODNOTA" AS BIGINT) AS chodnota,
    CAST("OKRSEK" AS BIGINT) AS okrsek,
    CAST("KC1" AS BIGINT) AS kc1,
    "NAZEVOKRSK" AS nazevokrsk,
    "TYPURADU" AS typuradu,
    CAST("KODZEME" AS BIGINT) AS kodzeme,
    "ZKRZEME" AS zkrzeme,
    "NAZEVZEME" AS nazevzeme,
    "SVETADIL" AS svetadil,
    "ADRESA" AS adresa,
    CAST("CASPOSUN" AS BIGINT) AS casposun,
    "NAZEVOKRSA" AS nazevokrsa,
    "NAZEVZEMEA" AS nazevzemea
FROM "czech-statistical-office-prez2018cis"
