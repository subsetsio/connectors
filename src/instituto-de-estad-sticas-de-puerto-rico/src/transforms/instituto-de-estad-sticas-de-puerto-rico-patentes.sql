-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Número de patente" AS n_mero_de_patente,
    "Tipo de patentes" AS tipo_de_patentes,
    CAST("Año de solicitud" AS BIGINT) AS a_o_de_solicitud,
    CAST("Mes de solicitud" AS BIGINT) AS mes_de_solicitud,
    CAST("Año de emisión" AS BIGINT) AS a_o_de_emisi_n,
    CAST("Mes de emisión" AS BIGINT) AS mes_de_emisi_n,
    CAST("Día de emisión" AS BIGINT) AS d_a_de_emisi_n,
    "Clase de Patente" AS clase_de_patente,
    "Subclase de Patente" AS subclase_de_patente,
    "Descripción de clase de Patente" AS descripci_n_de_clase_de_patente,
    "Nombre del primer inventor" AS nombre_del_primer_inventor,
    "Municipio del inventor" AS municipio_del_inventor,
    "Estado o pais del inventor" AS estado_o_pais_del_inventor,
    CAST("Identificación del primer dueño" AS BIGINT) AS identificaci_n_del_primer_due_o,
    CAST("Código de tipo de propiedad" AS BIGINT) AS c_digo_de_tipo_de_propiedad,
    "Primer dueño nombrado" AS primer_due_o_nombrado,
    "Tipo de dueño" AS tipo_de_due_o
FROM "instituto-de-estad-sticas-de-puerto-rico-patentes"
