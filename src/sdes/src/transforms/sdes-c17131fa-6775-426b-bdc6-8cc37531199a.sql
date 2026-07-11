-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "ZONE_CODE" AS zone_code,
    "ZONE_LIBELLE" AS zone_libelle,
    "PCS_CODE" AS pcs_code,
    "PCS_LIBELLE" AS pcs_libelle,
    "AGE" AS age,
    "ACHAT" AS achat,
    "NB_MAISONS" AS nb_maisons,
    "PM_MOY" AS pm_moy,
    "PMM2_MOY" AS pmm2_moy
FROM "sdes-c17131fa-6775-426b-bdc6-8cc37531199a"
