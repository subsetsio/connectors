-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "unit_measure",
    "statistical_operation",
    "inst_type_edu",
    "education_lev",
    "pers_type",
    "pers_qual_lev",
    "pers_exp_lev",
    "obs_status",
    "unit_mult",
    "price_base",
    "base_per",
    "currency",
    "ref_period",
    "decimals",
    "value"
FROM "oecd-oecd.edu.imep:dsd-eag-sal-sta@df-tch"
