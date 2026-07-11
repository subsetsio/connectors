-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FICHE" AS fiche,
    "LIBELLE_FICHE" AS libelle_fiche,
    "SECTEUR" AS secteur,
    "DEP_CODE" AS dep_code,
    "DEP_LIBELLE" AS dep_libelle,
    "ANNEE_FACTURATION" AS annee_facturation,
    "NB_DOSSIERS" AS nb_dossiers,
    "ECO_NRJ_KWHCUMAC" AS eco_nrj_kwhcumac,
    "ECO_NRJ_PRECARITE_KWHCUMAC" AS eco_nrj_precarite_kwhcumac
FROM "sdes-e9ceb45b-ff99-4fdd-8fbb-c3cda6caad0f"
