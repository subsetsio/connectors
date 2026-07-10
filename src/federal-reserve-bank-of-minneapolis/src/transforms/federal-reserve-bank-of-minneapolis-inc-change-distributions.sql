-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix geography types, demographic group variables, samples, income concepts, and one-year versus five-year horizons; filter these dimensions before comparing or aggregating values.
SELECT
    "level",
    "lag",
    "y0",
    "y1",
    "samp",
    "inc_var",
    "geo_var",
    "geo_var_val",
    "geo_abb",
    "group_var",
    "group_var_val",
    "pctl_y0",
    "pctl_y1",
    "value"
FROM "federal-reserve-bank-of-minneapolis-inc-change-distributions"
