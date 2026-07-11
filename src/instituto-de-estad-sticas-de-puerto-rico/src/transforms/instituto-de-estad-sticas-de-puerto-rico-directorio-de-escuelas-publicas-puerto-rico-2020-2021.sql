-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Región" AS regi_n,
    "Distrito" AS distrito,
    "Municipio Escolar" AS municipio_escolar,
    "Código" AS c_digo,
    "Escuela" AS escuela,
    CAST("Latitud" AS DOUBLE) AS latitud,
    CAST("Longitud" AS DOUBLE) AS longitud,
    "Status" AS status,
    "Nivel" AS nivel,
    "Grado que ofrece" AS grado_que_ofrece,
    "Montessori" AS montessori,
    CAST("Total M1Certificada" AS BIGINT) AS total_m1certificada,
    CAST("Total M1Activa" AS BIGINT) AS total_m1activa,
    CAST("Estrellas" AS BIGINT) AS estrellas,
    CAST("Puntuación" AS DOUBLE) AS puntuaci_n,
    "Clasificación ESSA" AS clasificaci_n_essa,
    CAST("Tasa de Deserción" AS DOUBLE) AS tasa_de_deserci_n,
    "Teléfono" AS tel_fono,
    "Dirección Física" AS direcci_n_f_sica,
    "Pueblo" AS pueblo,
    "Estado" AS estado,
    "Zipcode" AS zipcode,
    "Email" AS email,
    "Año_ID" AS a_o_id
FROM "instituto-de-estad-sticas-de-puerto-rico-directorio-de-escuelas-publicas-puerto-rico-2020-2021"
