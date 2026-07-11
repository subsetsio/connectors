-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "EPCI" AS epci,
    "TYPE_LGT" AS type_lgt,
    "LOG_AUT" AS log_aut,
    "LOG_COM" AS log_com,
    "SDP_AUT" AS sdp_aut,
    "SDP_COM" AS sdp_com
FROM "sdes-cb3c0612-e7d9-4a87-91be-cc0fb6448a4f"
