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
    "NB_TERRAINS" AS nb_terrains,
    "PT_MOY" AS pt_moy,
    "PTM2_MOY" AS ptm2_moy
FROM "sdes-a7e5426b-fee3-4eaa-a303-5eb34f4f2835"
