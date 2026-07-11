-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OPERATEUR" AS operateur,
    "ANNEE" AS annee,
    "FILIERE" AS filiere,
    "TYPE" AS type,
    "CODE" AS code,
    "CONSOA" AS consoa,
    "PDLA" AS pdla,
    "INDQUALA" AS indquala,
    "CONSOI" AS consoi,
    "PDLI" AS pdli,
    "INDQUALI" AS indquali,
    "CONSOT" AS consot,
    "PDLT" AS pdlt,
    "INDQUALT" AS indqualt,
    "CONSOR" AS consor,
    "PDLR" AS pdlr,
    "INDQUALR" AS indqualr,
    "CONSONA" AS consona,
    "PDLNA" AS pdlna,
    "INDQUALNA" AS indqualna,
    "THERMOR" AS thermor,
    "PARTR" AS partr
FROM "sdes-93e51ae0-effa-4c39-bcb5-9f94fc423c98"
