-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("ID_CONSOLIDADO" AS BIGINT) AS id_consolidado,
    CAST("?Con_cual_genero_se_identifica?_-PD_1" AS BIGINT) AS con_cual_genero_se_identifica_pd_1,
    CAST("Senale_en_que_rango_de_edad_se_encuentra-PD_2" AS BIGINT) AS senale_en_que_rango_de_edad_se_encuentra_pd_2,
    CAST("Pregunta_Etnia_1-PD_3" AS BIGINT) AS pregunta_etnia_1_pd_3,
    CAST("Pregunta_Etnia_2-PD_4" AS BIGINT) AS pregunta_etnia_2_pd_4,
    CAST("Pregunta_Localidad_1-PD_5" AS BIGINT) AS pregunta_localidad_1_pd_5,
    CAST("Pregunta_Localidad_2-PD_6" AS BIGINT) AS pregunta_localidad_2_pd_6,
    CAST("Pregunta_Localidad_3-PD_7" AS BIGINT) AS pregunta_localidad_3_pd_7,
    CAST("Por_favor_indique_si_reside_en_una_zona_urbana_poblacion_con" AS BIGINT) AS por_favor_indique_si_reside_en_una_zona_urbana_poblacion_con,
    CAST("Usted_se_describiria_como_perteneciendo_a_la_clase...-PD_9" AS BIGINT) AS usted_se_describiria_como_perteneciendo_a_la_clase_pd_9,
    "PAIS" AS pais,
    CAST("SERVICIO" AS BIGINT) AS servicio,
    CAST("Ano_Texto" AS BIGINT) AS ano_texto,
    CAST("Ano_Fecha" AS BIGINT) AS ano_fecha,
    "CANAL" AS canal,
    "Pregunta_Grupo" AS pregunta_grupo,
    "Variable" AS variable,
    "Pregunta_Texto" AS pregunta_texto,
    "Codigo" AS codigo,
    CAST("Respuesta_Rango_de_puntuacion" AS BIGINT) AS respuesta_rango_de_puntuacion,
    "source_resource"
FROM "idb-public-management-evaluation-tool-2007-2013"
