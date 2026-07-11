-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Licencia" AS licencia,
    "Institución" AS instituci_n,
    "Dirección física" AS direcci_n_f_sica,
    "Pueblo físico" AS pueblo_f_sico,
    "Zipcode físico" AS zipcode_f_sico,
    "Dirección postal" AS direcci_n_postal,
    "Pueblo postal" AS pueblo_postal,
    "Zipcode postal" AS zipcode_postal,
    "Teléfono" AS tel_fono,
    "Correo electrónico" AS correo_electr_nico,
    "Fax primario" AS fax_primario,
    "Nombre del director" AS nombre_del_director,
    "Masc" AS masc,
    "Fem" AS fem,
    "Total" AS total
FROM "instituto-de-estad-sticas-de-puerto-rico-directorio-de-instituciones-post-secundarias-tecnico-vocacionales-en-puerto-rico"
