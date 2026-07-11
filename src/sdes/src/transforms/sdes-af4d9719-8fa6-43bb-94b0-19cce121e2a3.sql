-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "ZONE_CODE" AS zone_code,
    "ZONE_LIBELLE" AS zone_libelle,
    "CHAUFFAGE" AS chauffage,
    "FINITION" AS finition,
    "ACHAT" AS achat,
    "NB_MAISONS" AS nb_maisons,
    "PM_MOY" AS pm_moy,
    "PMM2_MOY" AS pmm2_moy
FROM "sdes-af4d9719-8fa6-43bb-94b0-19cce121e2a3"
