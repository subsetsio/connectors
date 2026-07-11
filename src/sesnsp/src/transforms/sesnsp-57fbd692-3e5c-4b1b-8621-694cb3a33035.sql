-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Municipal incidence counts are monthly offense counts at the municipality grain; compare with the state incidence table only after accounting for the different geographic grain.
SELECT
    "anio",
    "clave_ent",
    "entidad",
    "cve_municipio",
    "municipio",
    "bien_juridico_afectado",
    "tipo_delito",
    "subtipo_delito",
    "modalidad",
    "mes",
    "fecha",
    "incidencia_delictiva"
FROM "sesnsp-57fbd692-3e5c-4b1b-8621-694cb3a33035"
