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
    "TIPO DE NORMA" AS tipo_de_norma,
    "Identificacion Norma" AS identificacion_norma,
    "DESCRIPCION MINIMA" AS descripcion_minima,
    "FECHA" AS fecha,
    "ENLACE A LA NORMA" AS enlace_a_la_norma,
    "__source_package_id" AS source_package_id,
    "__source_resource_id" AS source_resource_id,
    "__source_resource_name" AS source_resource_name,
    "__source_resource_url" AS source_resource_url,
    "__source_row_number" AS source_row_number
FROM "instituto-nacional-de-estad-stica-ine-marco-juridico-ine"
