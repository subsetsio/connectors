-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "state",
    "parlimen",
    "lf",
    "lf_employed",
    "lf_unemployed",
    "lf_outside",
    "u_rate",
    "p_rate",
    "ep_ratio"
FROM "dosm-lfs-parlimen"
