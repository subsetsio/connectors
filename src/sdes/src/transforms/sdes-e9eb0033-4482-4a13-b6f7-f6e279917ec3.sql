-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "DEPARTEMENT_CODE" AS departement_code,
    "DEPARTEMENT_LIBELLE" AS departement_libelle,
    "DESTINATION" AS destination,
    "SDP_AUT" AS sdp_aut,
    "SDP_COM" AS sdp_com
FROM "sdes-e9eb0033-4482-4a13-b6f7-f6e279917ec3"
