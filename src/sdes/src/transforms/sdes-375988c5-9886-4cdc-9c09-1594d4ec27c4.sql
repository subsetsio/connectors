-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "MOIS" AS mois,
    "NAT_SERIES" AS nat_series,
    "DESTINATION" AS destination,
    "SDP_AUT" AS sdp_aut,
    "SDP_COM" AS sdp_com
FROM "sdes-375988c5-9886-4cdc-9c09-1594d4ec27c4"
