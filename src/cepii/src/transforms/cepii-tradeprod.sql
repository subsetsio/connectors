-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows combine production, tariff, and bilateral trade fields by industry; only trade-value fields are additive.
SELECT
    "year",
    "iso3_tp_o",
    "iso3_tp_d",
    "pref",
    "mfn",
    "tariff",
    "trade_sq_iy",
    "trade_sq_yr",
    "flag_extra_neg",
    "flag_extra_cty",
    "flag_extra_avg",
    "industry"
FROM "cepii-tradeprod"
