-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Victim counts are reported at the monthly state by offense-classification, sex, and age-range grain; aggregate only after choosing the demographic and offense categories needed for the question.
SELECT
    "anio",
    "clave_ent",
    "entidad",
    "bien_juridico_afectado",
    "tipo_delito",
    "subtipo_delito",
    "modalidad",
    "sexo",
    "rango_edad",
    "mes",
    "fecha",
    "victimas"
FROM "sesnsp-386f17d2-a488-4da2-9c85-99765b5a9cdc"
