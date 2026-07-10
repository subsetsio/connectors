-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    "district",
    "date",
    "lf",
    "lf_employed",
    "lf_unemployed",
    "lf_outside",
    "p_rate",
    "u_rate",
    "ep_ratio"
FROM "dosm-lfs-district"
