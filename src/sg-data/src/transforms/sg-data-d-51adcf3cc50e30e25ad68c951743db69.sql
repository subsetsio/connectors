-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "residential_status",
    "user_type",
    "inst_cap_mwp",
    "inst_cap_mwac"
FROM "sg-data-d-51adcf3cc50e30e25ad68c951743db69"
