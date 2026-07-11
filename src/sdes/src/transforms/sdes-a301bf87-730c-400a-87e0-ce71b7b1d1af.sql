-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "MOIS" AS mois,
    "DEPARTEMENT_CODE" AS departement_code,
    "DEPARTEMENT_LIBELLE" AS departement_libelle,
    "DESTINATION" AS destination,
    "SDP_AUT" AS sdp_aut,
    "SDP_COM" AS sdp_com
FROM "sdes-a301bf87-730c-400a-87e0-ce71b7b1d1af"
