-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Municipio" AS municipio,
    CAST("Año" AS BIGINT) AS a_o,
    CAST("Alfabetismo (por ciento)" AS DOUBLE) AS alfabetismo_por_ciento,
    CAST("Tasa de desempleo (por ciento)" AS DOUBLE) AS tasa_de_desempleo_por_ciento,
    "Color" AS color,
    "Población de 65000 o más" AS poblaci_n_de_65000_o_m_s,
    CAST("Población" AS BIGINT) AS poblaci_n,
    CAST("Tasa de participación laboral (por ciento)" AS DOUBLE) AS tasa_de_participaci_n_laboral_por_ciento,
    CAST("Mediana de ingreso" AS BIGINT) AS mediana_de_ingreso,
    CAST("Población femenina (por ciento)" AS DOUBLE) AS poblaci_n_femenina_por_ciento,
    CAST("Casados (por ciento de 15 años o más)" AS DOUBLE) AS casados_por_ciento_de_15_a_os_o_m_s,
    CAST("Solteros (por ciento de 15 años o más)" AS DOUBLE) AS solteros_por_ciento_de_15_a_os_o_m_s,
    CAST("Población de 5-17 años (por ciento)" AS DOUBLE) AS poblaci_n_de_5_17_a_os_por_ciento,
    CAST("Población de 5 años (por ciento)" AS DOUBLE) AS poblaci_n_de_5_a_os_por_ciento,
    CAST("Mediana de valor de vivienda (miles de $)" AS BIGINT) AS mediana_de_valor_de_vivienda_miles_de,
    CAST("Viviendas alquiladas (por ciento)" AS DOUBLE) AS viviendas_alquiladas_por_ciento,
    CAST("Años de escolaridad (mediana)" AS DOUBLE) AS a_os_de_escolaridad_mediana,
    CAST("Promedio de ingreso familiar" AS DOUBLE) AS promedio_de_ingreso_familiar,
    CAST("Familias bajo el nivel de pobreza (por ciento)" AS DOUBLE) AS familias_bajo_el_nivel_de_pobreza_por_ciento,
    CAST("Vivienda inadecuada (por ciento)" AS BIGINT) AS vivienda_inadecuada_por_ciento,
    CAST("Población urbana (por ciento)" AS DOUBLE) AS poblaci_n_urbana_por_ciento
FROM "instituto-de-estad-sticas-de-puerto-rico-datos-municipales"
