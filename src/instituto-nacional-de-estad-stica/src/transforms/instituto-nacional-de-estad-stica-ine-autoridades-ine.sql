-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OID" AS oid,
    "Tipo Organismo" AS tipo_organismo,
    "INCISO" AS inciso,
    "UE" AS ue,
    "Nombre Inciso" AS nombre_inciso,
    "Nombre UE" AS nombre_ue,
    "Nombre Organismo" AS nombre_organismo,
    CAST("ID UNIDAD" AS BIGINT) AS id_unidad,
    "NOMBRE UNIDAD" AS nombre_unidad,
    "CARGO" AS cargo,
    "NOMBRE" AS nombre,
    "DIRECCION" AS direccion,
    "CORREO INSTITUCIONAL" AS correo_institucional,
    CAST("TELEFONO" AS BIGINT) AS telefono,
    "__source_package_id" AS source_package_id,
    "__source_resource_id" AS source_resource_id,
    "__source_resource_name" AS source_resource_name,
    "__source_resource_url" AS source_resource_url,
    "__source_row_number" AS source_row_number
FROM "instituto-nacional-de-estad-stica-ine-autoridades-ine"
