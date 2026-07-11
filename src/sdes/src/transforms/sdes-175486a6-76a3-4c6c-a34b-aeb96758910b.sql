-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "MOIS" AS mois,
    "TYPE_LGT" AS type_lgt,
    "NAT_SERIES" AS nat_series,
    "LOG_AUT" AS log_aut,
    "LOG_COM" AS log_com,
    "SDP_AUT" AS sdp_aut,
    "SDP_COM" AS sdp_com
FROM "sdes-175486a6-76a3-4c6c-a34b-aeb96758910b"
