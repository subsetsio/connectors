-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "ZONE_CODE" AS zone_code,
    "ZONE_LIBELLE" AS zone_libelle,
    "NB_TERRAINS" AS nb_terrains,
    "PTM2_MOY" AS ptm2_moy,
    "PTM2_Q1" AS ptm2_q1,
    "PTM2_MED" AS ptm2_med,
    "PTM2_Q3" AS ptm2_q3,
    "SURFT_MOY" AS surft_moy,
    "PT_MOY" AS pt_moy
FROM "sdes-7b0b1184-f92e-4f8a-8a6a-19b4b23d5118"
