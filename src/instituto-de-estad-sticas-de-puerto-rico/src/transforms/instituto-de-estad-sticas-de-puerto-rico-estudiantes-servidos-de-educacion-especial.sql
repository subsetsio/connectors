-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "MUNICIPIO_ESCOLAR" AS municipio_escolar,
    "MUNICIPIO_LOCATION" AS municipio_location,
    CAST("AUTISMO" AS BIGINT) AS autismo,
    CAST("DAÑO CEREBRAL POR TRAUMA" AS BIGINT) AS da_o_cerebral_por_trauma,
    CAST("DISTURBIOS EMOCIONALES" AS BIGINT) AS disturbios_emocionales,
    CAST("IMPEDIMENTOS MÚLTIPLES" AS BIGINT) AS impedimentos_m_ltiples,
    CAST("IMPEDIMENTOS VISUALES" AS BIGINT) AS impedimentos_visuales,
    CAST("OTROS PROBLEMAS DE SALUD" AS BIGINT) AS otros_problemas_de_salud,
    CAST("PROBLEMAS AUDITIVOS" AS BIGINT) AS problemas_auditivos,
    "PROBLEMAS DE HABLA Y LENGUAJE" AS problemas_de_habla_y_lenguaje,
    "PROBLEMAS ESPECÍFICOS DE APRENDIZAJE" AS problemas_espec_ficos_de_aprendizaje,
    CAST("PROBLEMAS ORTOPÉDICOS" AS BIGINT) AS problemas_ortop_dicos,
    CAST("DEFICIENCIA INTELECTUAL" AS BIGINT) AS deficiencia_intelectual,
    CAST("RETRASO EN EL DESARROLLO" AS BIGINT) AS retraso_en_el_desarrollo,
    CAST("SORDO CIEGO" AS BIGINT) AS sordo_ciego,
    "TOTAL" AS total,
    "AÑO ESCOLAR" AS a_o_escolar,
    "PUEBLO" AS pueblo
FROM "instituto-de-estad-sticas-de-puerto-rico-estudiantes-servidos-de-educacion-especial"
