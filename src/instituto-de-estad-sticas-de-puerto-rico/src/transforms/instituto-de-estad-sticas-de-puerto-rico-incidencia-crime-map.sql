-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Addr_type" AS addr_type,
    "KeyField" AS keyfield,
    "Street" AS street,
    "Zone" AS zone,
    "Dirección Estandarizada" AS direcci_n_estandarizada,
    "Estructura" AS estructura,
    "Fecha Ocurrencia" AS fecha_ocurrencia,
    "Delito NIBRS" AS delito_nibrs,
    CAST("Delito Tipo I" AS BIGINT) AS delito_tipo_i,
    "Hora Ocurrencia" AS hora_ocurrencia,
    CAST("Día de la semana" AS BIGINT) AS d_a_de_la_semana,
    CAST("km" AS DOUBLE) AS km,
    "Match_addr" AS match_addr,
    "Match_type" AS match_type,
    CAST("Carretera" AS BIGINT) AS carretera,
    CAST("OBJECTID" AS BIGINT) AS objectid,
    "observaciones hechos" AS observaciones_hechos,
    "GlobalID" AS globalid
FROM "instituto-de-estad-sticas-de-puerto-rico-incidencia-crime-map"
