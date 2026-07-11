-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are budget-execution line items; avoid summing across execution, project, auxiliary, and assignment dimensions unless that aggregation is intended.
SELECT
    "OID" AS oid,
    "Tipo Organismo" AS tipo_organismo,
    "INCISO" AS inciso,
    "UE" AS ue,
    "Nombre Inciso" AS nombre_inciso,
    "Nombre UE" AS nombre_ue,
    "Nombre Organismo" AS nombre_organismo,
    "DIVISION" AS division,
    "DEPARTAMENTO" AS departamento,
    CAST("PROGRAMA" AS BIGINT) AS programa,
    CAST("PROYECTO" AS BIGINT) AS proyecto,
    CAST("AÑO" AS BIGINT) AS ano,
    "MES" AS mes,
    CAST("TIPO DE GASTO" AS BIGINT) AS tipo_de_gasto,
    CAST("AUXILIAR" AS BIGINT) AS auxiliar,
    "FUENTE DE FINANCIAMENTO" AS fuente_de_financiamiento,
    "ASIGNACION" AS asignacion,
    CAST("EJECUCION" AS BIGINT) AS ejecucion,
    "__source_package_id" AS source_package_id,
    "__source_resource_id" AS source_resource_id,
    "__source_resource_name" AS source_resource_name,
    "__source_resource_url" AS source_resource_url,
    "__source_row_number" AS source_row_number
FROM "instituto-nacional-de-estad-stica-ine-presupuesto-ine"
