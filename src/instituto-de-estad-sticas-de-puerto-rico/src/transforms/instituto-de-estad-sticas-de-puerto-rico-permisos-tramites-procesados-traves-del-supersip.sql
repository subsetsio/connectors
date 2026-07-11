-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "NUM_TRAMITE" AS num_tramite,
    "PERMIT_TYPE" AS permit_type,
    strptime("CREATION_DATE", '%m/%d/%Y')::DATE AS creation_date,
    "PAID" AS paid,
    "PROJECT_NAME" AS project_name,
    "STATUS" AS status,
    "CATASTRO" AS catastro,
    "COORDX" AS coordx,
    "COORDY" AS coordy,
    "COORD_X_Y" AS coord_x_y,
    strptime("LAST_UPDATED", '%m/%d/%Y')::DATE AS last_updated,
    "ESTADO" AS estado,
    CAST("YEAR" AS BIGINT) AS year,
    "MES" AS mes,
    "MUNICIPIO" AS municipio,
    "TIPO_USO" AS tipo_uso,
    "PUBLICO_PRIVADO" AS publico_privado,
    "DESCRIPTION" AS description,
    "TIPO_ZONA" AS tipo_zona,
    "costo_estimado"
FROM "instituto-de-estad-sticas-de-puerto-rico-permisos-tramites-procesados-traves-del-supersip"
