-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "end_of_month",
    "nominal_gdp",
    "real_gdp",
    "gov_consol_bal",
    "composite_cpi",
    "unemploy_rate",
    "curr_acc_bal",
    "fc_reserve"
FROM "hkma-economic-statistics"
