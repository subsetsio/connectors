-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "DEP_CODE" AS dep_code,
    "DEP_LIBELLE" AS dep_libelle,
    "NB_EPL_TRANCHES" AS nb_epl_tranches,
    "SURFACE_TRANCHES" AS surface_tranches,
    "DENSITE_TRANCHES" AS densite_tranches
FROM "sdes-1bc6fe23-5b60-4e86-b8ab-699ff0d64b65"
