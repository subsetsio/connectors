-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "MOIS" AS mois,
    "DEPARTEMENT_CODE" AS departement_code,
    "DEPARTEMENT_LIBELLE" AS departement_libelle,
    "TYPE_LGT" AS type_lgt,
    "LOG_AUT" AS log_aut,
    "LOG_COM" AS log_com,
    "SDP_AUT" AS sdp_aut,
    "SDP_COM" AS sdp_com
FROM "sdes-d264957b-c6d2-4efa-bf5e-6a8da836550a"
