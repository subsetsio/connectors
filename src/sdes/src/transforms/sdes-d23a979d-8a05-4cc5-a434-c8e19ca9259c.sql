-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "ZONE_CODE" AS zone_code,
    "ZONE_LIBELLE" AS zone_libelle,
    "NB_MAISONS" AS nb_maisons,
    "PMM2_MOY" AS pmm2_moy,
    "PMM2_Q1" AS pmm2_q1,
    "PMM2_MED" AS pmm2_med,
    "PMM2_Q3" AS pmm2_q3,
    "SURFM_MOY" AS surfm_moy,
    "PM_MOY" AS pm_moy
FROM "sdes-d23a979d-8a05-4cc5-a434-c8e19ca9259c"
