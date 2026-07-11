-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table combines remuneration rows from more than one source CSV resource; preserve source resource context when comparing salary categories.
SELECT
    "OID" AS oid,
    "Tipo Organismo" AS tipo_organismo,
    "INCISO" AS inciso,
    "UE" AS ue,
    "Nombre Inciso" AS nombre_inciso,
    "Nombre UE" AS nombre_ue,
    "Nombre Organismo" AS nombre_organismo,
    "TIPO DE CARGO" AS tipo_de_cargo,
    "DENOMINACIÓN DEL CARGO" AS denominacion_del_cargo,
    "ESCALAFON" AS escalafon,
    CAST("GRADO" AS BIGINT) AS grado,
    CAST("REMUNERACION MENSUAL NOMINAL" AS BIGINT) AS remuneracion_mensual_nominal,
    CAST("Partida Alimentación" AS BIGINT) AS partida_alimentacion,
    CAST("Total mensual" AS BIGINT) AS total_mensual,
    "Observaciones" AS observaciones,
    "__source_package_id" AS source_package_id,
    "__source_resource_id" AS source_resource_id,
    "__source_resource_name" AS source_resource_name,
    "__source_resource_url" AS source_resource_url,
    "__source_row_number" AS source_row_number
FROM "instituto-nacional-de-estad-stica-ine-remuneraciones-ine"
