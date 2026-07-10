-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix within-group and across-group share definitions in `grp_type` along with multiple geography, demographic, sample, and income dimensions; filter those fields before comparing shares.
SELECT
    "level",
    "year",
    "samp",
    "inc_var",
    "geo_var",
    "geo_var_val",
    "geo_abb",
    "group_var",
    "group_var_val",
    "grp_type",
    "percentile",
    "proportion"
FROM "federal-reserve-bank-of-minneapolis-inc-share"
