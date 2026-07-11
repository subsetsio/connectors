-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PRIXG_BRUT" AS prixg_brut,
    "CHANGE_DE" AS change_de,
    "PMI_CMS" AS pmi_cms,
    "PMI_BRUT_ET" AS pmi_brut_et,
    "PMI_BRUT_DB" AS pmi_brut_db,
    "PMI_RAFF" AS pmi_raff,
    "PME_ELE" AS pme_ele,
    "PRIXG_ELE" AS prixg_ele,
    "PRIXG_GAZ" AS prixg_gaz,
    "PRIXG_GAZ_PEG" AS prixg_gaz_peg
FROM "sdes-8d77c639-f1a7-4a72-b8fc-49d0a834c77e"
