-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "EPCI_CODE" AS epci_code,
    "EPCI_LIBELLE" AS epci_libelle,
    "NB_EPL_TRANCHES" AS nb_epl_tranches,
    "SURFACE_TRANCHES" AS surface_tranches,
    "DENSITE_TRANCHES" AS densite_tranches
FROM "sdes-c23ceaf6-afe3-4087-abc5-7d97e2218c7c"
