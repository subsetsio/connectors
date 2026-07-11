-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FICHE" AS fiche,
    "LIBELLE_FICHE" AS libelle_fiche,
    "SECTEUR" AS secteur,
    "EPCI_2024_CODE" AS epci_2024_code,
    "EPCI_2024_LIBELLE" AS epci_2024_libelle,
    "ANNEE_ENGAGEMENT" AS annee_engagement,
    "NB_DOSSIERS" AS nb_dossiers,
    "ECO_NRJ_KWHCUMAC" AS eco_nrj_kwhcumac,
    "ECO_NRJ_PRECARITE_KWHCUMAC" AS eco_nrj_precarite_kwhcumac
FROM "sdes-bb1f2879-f838-4a62-a7b4-be950f9db718"
