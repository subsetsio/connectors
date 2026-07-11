-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Caso" AS caso,
    "Trámite" AS tr_mite,
    strptime("Fecha de Radicación", '%m/%d/%Y')::DATE AS fecha_de_radicaci_n,
    CAST("Año de Radicación" AS BIGINT) AS a_o_de_radicaci_n,
    CAST("Mes de Radicación" AS DOUBLE) AS mes_de_radicaci_n,
    "Catastro" AS catastro,
    "Municipio" AS municipio,
    "Dirección" AS direcci_n,
    "Región" AS regi_n,
    "Status" AS status,
    "Adjudicado o Pendiente" AS adjudicado_o_pendiente,
    strptime("Fecha de Adjudicación", '%m/%d/%Y')::DATE AS fecha_de_adjudicaci_n,
    "Siglas" AS siglas,
    "X" AS x,
    "Y" AS y,
    "Radicado Por PA" AS radicado_por_pa,
    "Nombre del Proyecto" AS nombre_del_proyecto,
    "Publico o Privado" AS publico_o_privado,
    "Rural o Urbano" AS rural_o_urbano,
    "Dueño del Proyecto" AS due_o_del_proyecto,
    "Location 1" AS location_1,
    CAST("Lat" AS DOUBLE) AS lat,
    CAST("Lon" AS DOUBLE) AS lon
FROM "instituto-de-estad-sticas-de-puerto-rico-pemas-permisos-de-uso"
