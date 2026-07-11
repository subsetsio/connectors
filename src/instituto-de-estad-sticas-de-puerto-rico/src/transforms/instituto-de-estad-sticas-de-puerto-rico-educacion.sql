-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Región" AS regi_n,
    CAST("Número de Incidente" AS BIGINT) AS n_mero_de_incidente,
    "Distrito" AS distrito,
    CAST("Código Escuela" AS BIGINT) AS c_digo_escuela,
    "Nombre Escuela" AS nombre_escuela,
    "Tipo de Incidente" AS tipo_de_incidente,
    CAST("Cantidad de Participantes" AS BIGINT) AS cantidad_de_participantes,
    CAST("K" AS BIGINT) AS k,
    CAST("1ro" AS BIGINT) AS "1ro",
    CAST("2do" AS BIGINT) AS "2do",
    CAST("3ro" AS BIGINT) AS "3ro",
    CAST("4to" AS BIGINT) AS "4to",
    CAST("5to" AS BIGINT) AS "5to",
    CAST("6to" AS BIGINT) AS "6to",
    CAST("7mo" AS BIGINT) AS "7mo",
    CAST("8vo" AS BIGINT) AS "8vo",
    CAST("9no" AS BIGINT) AS "9no",
    CAST("10mo" AS BIGINT) AS "10mo",
    CAST("11mo" AS BIGINT) AS "11mo",
    CAST("12mo" AS BIGINT) AS "12mo",
    CAST("SGE" AS BIGINT) AS sge,
    CAST("SGI" AS BIGINT) AS sgi,
    CAST("SGS" AS BIGINT) AS sgs
FROM "instituto-de-estad-sticas-de-puerto-rico-educacion"
