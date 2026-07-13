-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Figura_Tabla" AS figura_tabla,
    "Capitulo" AS capitulo,
    "Titulo" AS titulo,
    "Indicador" AS indicador,
    "Sub-indicador" AS sub_indicador,
    "Pais" AS pais,
    CAST("Ano" AS BIGINT) AS ano,
    CAST("Mes" AS BIGINT) AS mes,
    "Periodo" AS periodo,
    "Rubro" AS rubro,
    CAST("Valor_%" AS DOUBLE) AS valor,
    CAST("Valor_U$D" AS DOUBLE) AS valor_u_d,
    "Fuente" AS fuente,
    "Notas" AS notas,
    "source_resource"
FROM "idb-data-associated-with-informe-mercosur-n-20-2014-2015"
