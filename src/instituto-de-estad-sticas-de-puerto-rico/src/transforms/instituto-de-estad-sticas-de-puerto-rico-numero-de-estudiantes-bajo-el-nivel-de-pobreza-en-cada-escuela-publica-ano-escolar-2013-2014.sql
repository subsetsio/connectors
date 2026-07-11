-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Region" AS region,
    "Distrito" AS distrito,
    "Municipio Escolar" AS municipio_escolar,
    CAST("Codigo_Escuela" AS BIGINT) AS codigo_escuela,
    "Nombre_Escuela" AS nombre_escuela,
    CAST("Matricula_M1" AS BIGINT) AS matricula_m1,
    CAST("Matricula_M1_entre_5_17_anos" AS BIGINT) AS matricula_m1_entre_5_17_anos,
    CAST("M1_entre_5_17_BNP" AS BIGINT) AS m1_entre_5_17_bnp,
    CAST("Porcentaje_Estudiantes_Bajo_Nivel_ Pobreza" AS DOUBLE) AS porcentaje_estudiantes_bajo_nivel_pobreza
FROM "instituto-de-estad-sticas-de-puerto-rico-numero-de-estudiantes-bajo-el-nivel-de-pobreza-en-cada-escuela-publica-ano-escolar-2013-2014"
