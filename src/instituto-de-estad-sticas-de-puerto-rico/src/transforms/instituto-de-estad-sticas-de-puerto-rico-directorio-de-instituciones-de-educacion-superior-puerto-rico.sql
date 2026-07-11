-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Nombre de la Institución" AS nombre_de_la_instituci_n,
    "Unidad Académica" AS unidad_acad_mica,
    "Principal Ejecutivo" AS principal_ejecutivo,
    "Telefono" AS telefono,
    "Dirección Pág Web" AS direcci_n_p_g_web,
    "Correo Electrónico" AS correo_electr_nico,
    "Dirección Física" AS direcci_n_f_sica,
    "Dirección Física 2" AS direcci_n_f_sica_2,
    "Pueblo" AS pueblo
FROM "instituto-de-estad-sticas-de-puerto-rico-directorio-de-instituciones-de-educacion-superior-puerto-rico"
