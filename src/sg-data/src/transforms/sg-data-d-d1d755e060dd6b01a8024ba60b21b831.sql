-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "residential_status",
    "seasonally_adj_unemp_rate",
    "non_seasonally_adj_unemp_rate"
FROM "sg-data-d-d1d755e060dd6b01a8024ba60b21b831"
