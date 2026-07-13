-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Pais_EN" AS pais_en,
    "Pais_ES" AS pais_es,
    "Dimension_EN" AS dimension_en,
    "Dimension_ES" AS dimension_es,
    "Factor_EN" AS factor_en,
    "Factor_ES" AS factor_es,
    "Indicador_EN" AS indicador_en,
    "Indicador_ES" AS indicador_es,
    "Indicador_Nombre_EN" AS indicador_nombre_en,
    "Indicador_Nombre_ES" AS indicador_nombre_es,
    CAST("Anio_Texto" AS BIGINT) AS anio_texto,
    CAST("Anio_Fecha_y_Hora" AS BIGINT) AS anio_fecha_y_hora,
    CAST("Nivel_de_madurez" AS BIGINT) AS nivel_de_madurez,
    "Nivel_de_madurez_texto_EN" AS nivel_de_madurez_texto_en,
    "Nivel_de_madurez_texto_ES" AS nivel_de_madurez_texto_es,
    "source_resource"
FROM "idb-data-associated-with-advanced-experiences-in-cybersecurity-policies-and-pra"
