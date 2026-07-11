-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: State incidence counts are monthly offense counts at the state grain; compare with the municipal incidence table only after accounting for the different geographic grain.
SELECT
    "anio",
    "clave_ent",
    "entidad",
    "bien_juridico_afectado",
    "tipo_delito",
    "subtipo_delito",
    "modalidad",
    "mes",
    "fecha",
    "incidencia_delictiva",
    "entidad_federativa"
FROM "sesnsp-d9b2792a-33a2-4ea8-8527-210d9e99de5e"
