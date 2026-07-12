-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("OPERATEUR" AS VARCHAR) AS operateur,
    CAST("ANNEE" AS BIGINT) AS annee,
    CAST("FILIERE" AS VARCHAR) AS filiere,
    CAST("TYPE" AS VARCHAR) AS type,
    CAST("CODE" AS VARCHAR) AS code,
    CAST("CONSOA" AS DOUBLE) AS consoa,
    CAST("PDLA" AS BIGINT) AS pdla,
    CAST("INDQUALA" AS DOUBLE) AS indquala,
    CAST("CONSOI" AS DOUBLE) AS consoi,
    CAST("PDLI" AS BIGINT) AS pdli,
    CAST("INDQUALI" AS DOUBLE) AS indquali,
    CAST("CONSOT" AS DOUBLE) AS consot,
    CAST("PDLT" AS BIGINT) AS pdlt,
    CAST("INDQUALT" AS DOUBLE) AS indqualt,
    CAST("CONSOR" AS DOUBLE) AS consor,
    CAST("PDLR" AS BIGINT) AS pdlr,
    CAST("INDQUALR" AS DOUBLE) AS indqualr,
    CAST("CONSONA" AS DOUBLE) AS consona,
    CAST("PDLNA" AS BIGINT) AS pdlna,
    CAST("INDQUALNA" AS DOUBLE) AS indqualna,
    CAST("THERMOR" AS BIGINT) AS thermor,
    CAST("PARTR" AS DOUBLE) AS partr
FROM "sdes-91256d4d-037a-4df8-b6e2-12b6ab87e3a1"
