-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix geography types, demographic group variables, samples, and income concepts; the wide percentile columns are alternative measures for the same row dimensions rather than additive fields.
SELECT
    "year",
    "level",
    "samp",
    "inc_var",
    "geo_var",
    "geo_var_val",
    "geo_abb",
    "group_var",
    "group_var_val",
    "pctl10",
    "pctl25",
    "pctl50",
    "pctl75",
    "pctl90",
    "pctl95",
    "pctl98",
    "pctl99",
    "pctl99_9",
    "pctl99_99",
    "pctl99_999",
    "pce",
    "pctl10_adj",
    "pctl25_adj",
    "pctl50_adj",
    "pctl75_adj",
    "pctl90_adj",
    "pctl95_adj",
    "pctl98_adj",
    "pctl99_adj",
    "pctl99_9_adj",
    "pctl99_99_adj",
    "pctl99_999_adj"
FROM "federal-reserve-bank-of-minneapolis-pctl-of-inc"
