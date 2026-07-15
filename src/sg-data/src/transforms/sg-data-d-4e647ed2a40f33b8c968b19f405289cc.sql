-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "mth",
    "housing_type",
    "dwelling_type",
    "avg_mthly_hh_tg_consp_kwh"
FROM "sg-data-d-4e647ed2a40f33b8c968b19f405289cc"
