-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("VSTRANA" AS BIGINT) AS vstrana,
    "NAZEVCELK" AS nazevcelk,
    "NAZEV_STRV" AS nazev_strv,
    "ZKRATKAV30" AS zkratkav30,
    "ZKRATKAV8" AS zkratkav8,
    CAST("POCSTR_SLO" AS BIGINT) AS pocstr_slo,
    "SLOZENI" AS slozeni,
    "ZKRATKA_OF" AS zkratka_of,
    "TYPVS" AS typvs,
    "PLNYNAZEV" AS plnynazev
FROM "czech-statistical-office-kz2024cvs"
