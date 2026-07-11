-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "MOIS" AS mois,
    "REGION" AS region,
    "NAT_SERIES" AS nat_series,
    "DESTINATION" AS destination,
    "SDP_AUT" AS sdp_aut,
    "SDP_COM" AS sdp_com
FROM "sdes-b4da5bf2-4b1f-4a39-9d79-805777c29c5d"
