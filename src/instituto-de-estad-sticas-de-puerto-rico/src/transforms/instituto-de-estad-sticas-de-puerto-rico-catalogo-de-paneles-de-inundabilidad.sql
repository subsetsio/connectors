-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Número de Panel" AS n_mero_de_panel,
    "Fecha Vigencia Panel" AS fecha_vigencia_panel,
    CAST("Año Vigencia Panel" AS BIGINT) AS a_o_vigencia_panel,
    "Municipio" AS municipio,
    "Sector" AS sector,
    "Barrio" AS barrio,
    "Link a Imagen" AS link_a_imagen
FROM "instituto-de-estad-sticas-de-puerto-rico-catalogo-de-paneles-de-inundabilidad"
