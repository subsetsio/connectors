-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    strptime("MOIS", '%Y-%m')::DATE AS mois,
    "TYPE_CODE" AS type_code,
    "TYPE_LIBELLE" AS type_libelle,
    "COND_CODE" AS cond_code,
    "COND_LIBELLE" AS cond_libelle,
    "DIVNST_CODE" AS divnst_code,
    "DIVNST_LIBELLE" AS divnst_libelle,
    "PAV_CODE" AS pav_code,
    "PAV_LIBELLE" AS pav_libelle,
    "TONNES" AS tonnes,
    "TKM" AS tkm,
    "EVP" AS evp,
    "EVP_KM" AS evp_km
FROM "sdes-ad270003-70bc-4e45-a37c-06f36dcc56a5"
