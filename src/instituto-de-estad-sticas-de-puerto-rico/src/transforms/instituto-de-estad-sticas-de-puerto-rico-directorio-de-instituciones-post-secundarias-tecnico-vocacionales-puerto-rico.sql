-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Lic" AS lic,
    "Nombre de la institución" AS nombre_de_la_instituci_n,
    "Dirección Física" AS direcci_n_f_sica,
    "Pueblo físico" AS pueblo_f_sico,
    "Zip code físico" AS zip_code_f_sico,
    "Dirección postal" AS direcci_n_postal,
    "Pueblo postal" AS pueblo_postal,
    "Zip code postal" AS zip_code_postal,
    "Teléfono primario" AS tel_fono_primario,
    "Teléfono secundario" AS tel_fono_secundario,
    "Email primario" AS email_primario,
    "Email secundario" AS email_secundario,
    "Fax primario" AS fax_primario,
    "Fax secundario" AS fax_secundario,
    "Nombre del director" AS nombre_del_director,
    "Matricula total" AS matricula_total
FROM "instituto-de-estad-sticas-de-puerto-rico-directorio-de-instituciones-post-secundarias-tecnico-vocacionales-puerto-rico"
