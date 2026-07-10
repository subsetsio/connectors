-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix geography types, demographic group variables, samples, income concepts, and percentile thresholds; filter these dimensions before comparing population shares.
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
    "percentile",
    "proportion"
FROM "federal-reserve-bank-of-minneapolis-prop-share"
