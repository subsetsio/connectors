-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Región Agrícola" AS regi_n_agr_cola,
    "Producto" AS producto,
    CAST("Año" AS BIGINT) AS a_o,
    CAST("Fincas" AS BIGINT) AS fincas,
    CAST("Cosecha" AS BIGINT) AS cosecha,
    "Unidad" AS unidad,
    CAST("Ventas" AS BIGINT) AS ventas,
    CAST("Conteo" AS BIGINT) AS conteo
FROM "instituto-de-estad-sticas-de-puerto-rico-datos-del-tablero-indice-agricolas-resumen-censos-agricolas-2018-y-2022-por-regiones"
