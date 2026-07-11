-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Nombre" AS nombre,
    "Tipo de Facilidad" AS tipo_de_facilidad,
    CAST("Numero de Lic" AS BIGINT) AS numero_de_lic,
    "Dueño o Control" AS due_o_o_control,
    "Tipo de Acreditacion/numero" AS tipo_de_acreditacion_numero,
    "Direccion" AS direccion,
    "Telefono" AS telefono,
    "Pueblo" AS pueblo,
    CAST("Numero de Estaciones" AS BIGINT) AS numero_de_estaciones,
    CAST("Capacidad de Camamas Autorizadas" AS BIGINT) AS capacidad_de_camamas_autorizadas,
    CAST("Capacidad de Camas en Uso" AS BIGINT) AS capacidad_de_camas_en_uso
FROM "instituto-de-estad-sticas-de-puerto-rico-registro-de-hospitales-y-otras-facilidades-de-salud-en-puerto-rico"
